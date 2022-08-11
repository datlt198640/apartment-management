import * as React from "react";
import { useEffect, useState } from "react";
import { useSetRecoilState } from "recoil";
import { Row, Col, Button, Table, DatePicker, Typography, Select } from "antd";
import { DeleteOutlined, PlusOutlined } from "@ant-design/icons";
import Pagination, { defaultLinks } from "utils/components/table/Pagination";
import SearchInput from "utils/components/table/SearchInput";
import { DrawerAnt } from "utils/components/drawer";
import Utils from "utils/Utils";
import Dialog from "./dialog";
import { useDidMountEffect } from "utils/CustomHooks/useDidMountEffect";
import { urls, labels, messages } from "./config";
import {
  listMemberSt,
  listMemberEmailSt,
  listMemberPhoneNumberSt,
  listMemberShipTypeCheckInSt,
} from "./states";
import moment from "moment";
import { notification } from "antd";

const { RangePicker } = DatePicker;
const { Text } = Typography;
const { Option } = Select;

const FORMAT = "YYYY-MM-DD HH:mm";

const initialFilter = {
  is_check_out: 2,
  page: 1,
};

const validateFilter = (filter) => {
  for (let propName in filter) {
    if (filter[propName] === null || filter[propName] === undefined) {
      delete filter[propName];
    }
  }
  return filter;
};

const initialMemberInf = {
  phoneNumber: "",
  email: "",
  fullName: "",
  gender: "",
  dob: "",
  occupation: "",
  address: "",
  avatar: "",
  membership_type: "",
  register_date: "",
  expire_date: "",
};

export default function CheckInTable() {
  const [init, setInit] = useState(true);
  const [list, setList] = useState([]);
  const [ids, setIds] = useState([]);
  const [links, setLinks] = useState(defaultLinks);
  const [filter, setFilter] = useState(initialFilter);
  const [visible, setVisible] = useState(false);
  const [memberInf, setMemberInf] = useState(initialMemberInf);

  const setListMembershipType = useSetRecoilState(listMemberShipTypeCheckInSt);
  const setListMember = useSetRecoilState(listMemberSt);
  const setListMemberEmail = useSetRecoilState(listMemberEmailSt);
  const setListMemberPhoneNumber = useSetRecoilState(listMemberPhoneNumberSt);

  const onClose = () => {
    setVisible(false);
  };

  const convertIdToLabel = (data) => {
    const genderValue = [
      { value: 0, label: "Male" },
      { value: 1, label: "Female" },
    ];
    Utils.idToLabel(
      data.items,
      data.extra.list_membership_type,
      "membership_type"
    );
    Utils.idToLabel(data.items, data.extra.list_member_label, "member");
    Utils.idToLabel(data.items, genderValue, "gender");
  };

  const convert_date_format = (array, format = "YYYY-MM-DD HH:mm") => {
    for (let i = 0; i < array.length; i++) {
      array[i]["check_in"] = moment(array[i]["check_in"]).format(format);
      if (array[i]["check_out"] != null) {
        array[i]["check_out"] = moment(array[i]["check_out"]).format(format);
      }
    }
  };
  const convert_date_format_obj = (obj, format = "YYYY-MM-DD HH:mm") => {
    obj["check_in"] = moment(obj["check_in"]).format(format);
    if (obj["check_out"] != null) {
      obj["check_out"] = moment(obj["check_out"]).format(format);
    }
  };

  const openNotificationSuccess = (type, message) => {
    notification[type]({
      message: message,
    });
  };

  const getList =
    (showLoading = true) =>
    (url = "", params = {}) => {
      showLoading && Utils.toggleGlobalLoading();
      Utils.apiCall(url ? url : urls.crud, params)
        .then((resp) => {
          setLinks(resp.data.links);
          convertIdToLabel(resp.data);
          setListMember(resp.data.extra.list_member);
          setListMemberEmail(resp.data.extra.list_email);
          setListMemberPhoneNumber(resp.data.extra.list_phone_number);
          setListMembershipType(resp.data.extra.list_membership_type);
          convert_date_format(resp.data.items);
          setList(Utils.appendKey(resp.data.items));
        })
        .finally(() => {
          setInit(false);
          showLoading && Utils.toggleGlobalLoading(false);
        });
    };

  useEffect(() => {
    getList(false)();
  }, []);

  const onCheckOut = (id) => {
    const r = window.confirm(messages.checkOut);
    if (!r) return;

    const params = {
      check_out: Utils.getCurrentTime(),
    };
    Utils.toggleGlobalLoading(true);
    Utils.apiCall(`${urls.crud}${id}`, params, "put")
      .then((resp) => {
        const { data } = resp;
        const index = list.findIndex((item) => item.id === data.id);
        data.key = data.id;
        data["check_in"] = moment(data["check_in"]).format(FORMAT);
        data["check_out"] = moment(data["check_out"]).format(FORMAT);
        list[index] = data;
        setList([...list]);
      })
      .finally(() => Utils.toggleGlobalLoading(false));
    openNotificationSuccess("success", "Check Out Successfully");
  };

  const onBulkDelete = (ids) => {
    const r = window.confirm(messages.deleteMultiple);
    if (!r) return;

    Utils.toggleGlobalLoading(true);
    Utils.apiCall(`${urls.crud}?ids=${ids.join(",")}`, {}, "delete")
      .then(() => {
        setList([...list.filter((item) => !ids.includes(item.id))]);
      })
      .finally(() => Utils.toggleGlobalLoading(false));
  };

  const onChange = (data, id) => {
    convert_date_format_obj(data);
    if (!id) {
      setList([{ ...data, key: data.id }, ...list]);
    } else {
      const index = list.findIndex((item) => item.id === id);
      data.key = data.id;
      list[index] = data;
      setList([...list]);
    }
    openNotificationSuccess("success", "Check In Successfully");
  };

  const columns = [
    {
      key: "member",
      title: labels.member,
      dataIndex: "member",
      width: 120,
      render: (_text, record) => {
        return (
          <a
            type="default"
            htmlType="button"
            size="small"
            onClick={() => {
              setVisible(true);
              setMemberInf({
                phoneNumber: record.member_real_phone_number,
                email: record.member_real_email,
                fullName: record.member_real_name,
                gender: record.gender,
                dob: record.dob,
                occupation: record.occupation,
                address: record.address,
                avatar: record.avatar,
                membership_type: record.membership_type,
                register_date: record.register_date,
                expire_date: record.expire_date,
              });
            }}
          >
            {_text}
          </a>
        );
      },
    },
    {
      key: "member_email",
      title: labels.memberEmail,
      dataIndex: "member_email",
      render: (_text, record) => {
        return (
          <a href={`mailto: ${record.member_email}`}> {record.member_email}</a>
        );
      },
    },
    {
      key: "member_phone_number",
      title: labels.memberPhoneNumber,
      dataIndex: "member_phone_number",
      width: 140,
      render: (_text, record) => {
        return (
          <a href={`tel:${record.member_phone_number}`}>
            {" "}
            {record.member_phone_number}
          </a>
        );
      },
    },
    {
      key: "check_in",
      title: labels.check_in,
      dataIndex: "check_in",
    },
    {
      key: "check_out",
      title: labels.check_out,
      dataIndex: "check_out",
    },
    {
      key: "action",
      title: "Status",
      fixed: "right",
      width: 150,
      render: (_text, record) => (
        <span>
          <Button
            onClick={() => onCheckOut(record.id)}
            type="default"
            htmlType="button"
            disabled={record.check_out == null ? false : true}
          >
            Check out
          </Button>
        </span>
      ),
    },
  ];

  const rowSelection = {
    onChange: (ids) => {
      setIds(ids);
    },
  };

  // onchange date

  function setAndSendFilter(key, value) {
    let params = {};
    if (key == "is_check_out") {
      params = { ...filter, [key]: value };
    } else if (key == "check_in") {
      params = {
        ...filter,
        start_check_in: value[0]?.toISOString(),
        end_check_in: value[1]?.toISOString(),
      };
    } else if (key == "check_out") {
      params = {
        ...filter,
        start_check_out: value && value[0].toISOString(),
        end_check_out: value && value[1].toISOString(),
      };
    } else if (key == "search") {
      params = {
        ...filter,
        search: value,
      };
    }
    setFilter(params);
  }

  // useEffect(() => {
  //   getList()("", validateFilter(filter));
  // }, [filter]);

  useDidMountEffect(() => {
    getList()("", validateFilter(filter));
  }, [filter]);

  return (
    <div>
      <Row style={{ marginBottom: "1em" }}>
        <Col span={12}>
          <Row justify="start" align="middle">
            <Text strong style={{ width: "5em" }}>
              {" "}
              Search:{" "}
            </Text>
            <Col span={19}>
              <SearchInput
                onChange={(values) => setAndSendFilter("search", values)}
                placeHolder="Search for member's name, email, phone number"
              />
            </Col>
          </Row>
        </Col>
        <Col span={12} className="right">
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => Dialog.toggle()}
            style={{ marginRight: "1vw" }}
          >
            Add New
          </Button>
          <Button
            type="primary"
            danger
            icon={<DeleteOutlined />}
            disabled={!ids.length}
            onClick={() => onBulkDelete(ids)}
          >
            Delete
          </Button>
        </Col>
      </Row>
      <Row style={{ marginBottom: "1em" }}>
        <Col span={12}>
          <Row justify="start" align="middle">
            <Text strong style={{ width: "5em" }}>
              {" "}
              Check in:{" "}
            </Text>
            <Col span={19}>
              <RangePicker
                ranges={{
                  Today: [moment(), moment()],
                  "This Month": [
                    moment().startOf("month"),
                    moment().endOf("month"),
                  ],
                }}
                showTime
                format="YYYY/MM/DD HH:mm"
                onChange={(dates) => setAndSendFilter("check_in", dates)}
                style={{ width: "100%" }}
              />
            </Col>
          </Row>
        </Col>
        <Col span={12}>
          <Row justify="end" align="middle">
            <Text strong style={{ marginRight: "9px" }}>
              {" "}
              Check out:{" "}
            </Text>
            <Col span={19}>
              <RangePicker
                ranges={{
                  Today: [moment(), moment()],
                  "This Month": [
                    moment().startOf("month"),
                    moment().endOf("month"),
                  ],
                }}
                showTime
                format="YYYY/MM/DD HH:mm"
                onChange={(dates) => setAndSendFilter("check_out", dates)}
                style={{ width: "100%" }}
              />
            </Col>
          </Row>
        </Col>
      </Row>
      <Row style={{ marginBottom: "3em" }} justify="start" align="middle">
        <Text strong style={{ width: "5em" }}>
          Status:
        </Text>
        <Col span={19}>
          <Select
            defaultValue={2}
            style={{ minWidth: "12em" }}
            onChange={(value) => setAndSendFilter("is_check_out", value)}
          >
            <Option value={2}>All</Option>
            <Option value={0}>Have not check out yet</Option>
            <Option value={1}>Checked out</Option>
          </Select>
        </Col>
      </Row>
      <Table
        rowSelection={{
          type: "checkbox",
          ...rowSelection,
        }}
        columns={columns}
        dataSource={list}
        loading={init}
        scroll={{ x: 1000 }}
        pagination={false}
      />
      <Pagination
        next={links.next}
        prev={links.previous}
        onChange={getList()}
      />
      <DrawerAnt
        data={memberInf}
        visible={visible}
        onClose={onClose}
        placement="right"
      />
      <Dialog onChange={onChange} />
    </div>
  );
}

CheckInTable.displayName = "CheckInTable";
