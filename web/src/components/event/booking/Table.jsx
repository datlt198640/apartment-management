import * as React from "react";
import { useEffect, useState } from "react";
import { Row, Col, Button, Table, Typography } from "antd";
import SelectInput from "utils/components/ant_form/input/SelectInput";
import { DeleteOutlined } from "@ant-design/icons";
import Pagination, { defaultLinks } from "utils/components/table/Pagination";
import SearchInput from "utils/components/table/SearchInput";
import { DrawerAnt } from "utils/components/drawer";
import Utils from "utils/Utils";
import { useDidMountEffect } from "utils/CustomHooks/useDidMountEffect";
import { urls, labels, messages } from "./config";
import { listMemberEventSt, listEventSt, listEventBookingSt, listMemberShipTypeEventSt } from "./states";
import { useSetRecoilState, useRecoilState } from "recoil";

const { Text } = Typography;

const initialFilter = {
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
}

export default function BookingTable() {
  const [init, setInit] = useState(true);
  const [list, setList] = useState([]);
  const [ids, setIds] = useState([]);
  const [links, setLinks] = useState(defaultLinks);
  const [filter, setFilter] = useState(initialFilter);
  const [visible, setVisible] = useState(false);
  const [memberInf, setMemberInf] = useState(initialMemberInf);

  const setListMembershipType = useSetRecoilState(listMemberShipTypeEventSt);
  const setListMemberEvent = useSetRecoilState(listMemberEventSt);
  const setListEvent = useSetRecoilState(listEventSt);
  const setListEventBooking = useSetRecoilState(listEventBookingSt);
  // const setMemberShipTypeEventBooking = useSetRecoilState(listMemberShipTypeEventSt);
  const listEventBooking = useRecoilState(listEventBookingSt);

  const onClose = () => {
    setVisible(false);
  };


  const convertIdToLabel = (data) => {

    const genderValue =  [
      {value: 0, label: 'Male'},
      {value: 1, label: 'Female'},
    ]
    Utils.idToLabel(data.items, data.extra.list_membership_type, "membership_type");
    Utils.idToLabel(data.items, data.extra.list_event, "event");
    Utils.idToLabel(data.items, data.extra.list_member, "member");
    Utils.idToLabel(data.items, genderValue, "gender");
  };



  const getList =
    (showLoading = true) =>
    (url = "", params = {}) => {
      showLoading && Utils.toggleGlobalLoading();
      Utils.apiCall(url ? url : urls.crud, params)
        .then((resp) => {
          setLinks(resp.data.links);
          convertIdToLabel(resp.data);
          setListMemberEvent(resp.data.extra.list_member);
          setListEventBooking(resp.data.extra.list_event_booking);
          setListEvent(resp.data.extra.list_event);
          setListMembershipType(resp.data.extra.list_membership_type);
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

  const onDelete = (id) => {
    const r = window.confirm(messages.deleteOne);
    if (!r) return;

    Utils.toggleGlobalLoading(true);
    Utils.apiCall(`${urls.crud}${id}`, {}, "delete")
      .then(() => {
        setList([...list.filter((item) => item.id !== id)]);
      })
      .finally(() => Utils.toggleGlobalLoading(false));
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

  const columns = [
    {
      key: "event",
      title: labels.event,
      dataIndex: "event",
    },
    {
      key: "member",
      title: labels.member,
      dataIndex: "member",
      width: 120,
      render: (_text, record) => {
        return (
          <a type="default" htmlType="button" size="small" onClick={() => {
            setVisible(true)
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
            })
          }}
          >
            {_text}
          </a>
        );
      },
    },
    {
      key: "member_name",
      title: labels.memberName,
      dataIndex: "member_name",
    },
    {
      key: "phone_number",
      title: labels.phoneNumber,
      dataIndex: "phone_number",
      width: 140,
      render: (_text, record) => {
        return <a href={`tel:${record.phone_number}`}> {record.phone_number}</a>;
      },
    },
    {
      key: "email",
      title: labels.email,
      dataIndex: "email",
      render: (_text, record) => {
        return <a href={`mailto:${record.email}`}> {record.email}</a>;
      },
    },
    {
      key: "action",
      title: "",
      fixed: "right",
      width: 90,
      render: (_text, record) => (
        <span>
          <Button
            danger
            type="default"
            htmlType="button"
            icon={<DeleteOutlined />}
            size="small"
            onClick={() => onDelete(record.id)}
          />
        </span>
      ),
    },
  ];

  const rowSelection = {
    onChange: (ids) => {
      setIds(ids);
    },
  };

  // filter system
  function setAndSendFilter(key, value) {
    let params = {};
    if (key == "event") {
      params = { ...filter, [key]: value };
    } else if (key == "search") {
      params = {
        ...filter,
        [key]: value,
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
      <Row style={{ marginBottom: "30px" }} justify="start" align="middle" >
        <Col span={12}>
          <Row justify="start" align="middle">
            <Text strong style={{ minWidth: "4em" }}>
              Search:
            </Text>
            <Col span={19}>
              <SearchInput onChange={(value) => setAndSendFilter("search", value)} placeHolder="Search for event, member, and other information" />
            </Col>
          </Row>
        </Col>
        <Col span={12} className="right">
          <Button
            type="primary"
            danger
            icon={<DeleteOutlined />}
            disabled={!ids.length}
            onClick={() => onBulkDelete(ids)}
          >
            Xoá chọn
          </Button>
        </Col>
      </Row>
      <Row style={{ marginBottom: "30px" }} justify="start" align="middle" >
        <Col span={12}>
          <Row justify="start" align="middle">
            <Text strong style={{ width: "4em", minWidth: "4em" }}>
              Event:
            </Text>
            <Col span={19}>
              <SelectInput options={listEventBooking[0]} onChange={(event) => setAndSendFilter("event", event)} style={{width: "100%"}}/>
            </Col>
          </Row>
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
      <Pagination next={links.next} prev={links.previous} onChange={getList()} />
      <DrawerAnt data={memberInf} visible={visible} onClose={onClose} placement="right"  />
    </div>
  );
}

BookingTable.displayName = "BookingTable";
