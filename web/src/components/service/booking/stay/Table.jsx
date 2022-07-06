import * as React from "react";
import { useEffect, useState } from "react";
import { Row, Col, Button, Table, Typography } from "antd";
import { DeleteOutlined } from "@ant-design/icons";
import Pagination, { defaultLinks } from "utils/components/table/Pagination";
import SearchInput from "utils/components/table/SearchInput";
import { DrawerAnt } from "utils/components/drawer";
import Utils from "utils/Utils";
import { urls, labels, messages } from "./config";
import { listServiceSt, listMembershipTypeSt } from "../states";
import { useSetRecoilState } from "recoil";

const { Text } = Typography;

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
 
export default function BookingStayTable() {
  const [init, setInit] = useState(true);
  const [list, setList] = useState([]);
  const [ids, setIds] = useState([]);
  const [links, setLinks] = useState(defaultLinks);
  const [visible, setVisible] = useState(false);
  const [memberInf, setMemberInf] = useState(initialMemberInf);
  const setListService = useSetRecoilState(listServiceSt);
  const setListMembershipType = useSetRecoilState(listMembershipTypeSt);

  const onClose = () => {
    setVisible(false);
  };


  const convertIdToLabel = (data) => {

    const genderValue =  [
      {value: 0, label: 'Male'},
      {value: 1, label: 'Female'},
    ]
    Utils.idToLabel(data.items, data.extra.list_membership_type, "membership_type");
    Utils.idToLabel(data.items, data.extra.list_service, "service");
    Utils.idToLabel(data.items, data.extra.list_member, "member");
    Utils.idToLabel(data.items, genderValue, "gender");
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

  const getList =
    (showLoading = true) =>
    (url = "", params = {}) => {
      showLoading && Utils.toggleGlobalLoading();
      Utils.apiCall(url ? url : urls.crud, params)
        .then((resp) => {
          setLinks(resp.data.links);
          convertIdToLabel(resp.data);
          setListService(resp.data.extra.list_service);
          setListMembershipType(resp.data.extra.list_membership_type);
          setList(Utils.appendKey(resp.data.items));
        })
        .finally(() => {
          setInit(false);
          showLoading && Utils.toggleGlobalLoading(false);
        });
    };
  const searchList = (keyword) => {
    getList()("", keyword ? { search: keyword } : {});
  };

  useEffect(() => {
    getList(false)("", { type: 1 });
  }, []);

  const rowSelection = {
    onChange: (ids) => {
      setIds(ids);
    },
  };

  const columns = [
    {
      key: "service",
      title: labels.service,
      dataIndex: "service",
      width: 120,
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
      width: 120,
    },
    {
      key: "phone_number",
      title: labels.phoneNumber,
      dataIndex: "phone_number",
      width: 140,
    },
    {
      key: "email",
      title: labels.email,
      dataIndex: "email",
      width: 120,
    },
    {
      key: "adult",
      title: labels.adult,
      dataIndex: "adult",
      width: 120,
    },
    {
      key: "childs",
      title: labels.childs,
      dataIndex: "childs",
      width: 120,
    },
    {
      key: "check_in",
      title: labels.checkIn,
      dataIndex: "check_in",
      width: 120,
    },
    {
      key: "check_out",
      title: labels.checkOut,
      dataIndex: "check_out",
      width: 120,
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

  return (
    <div>
      <Row style={{ marginBottom: "30px" }}>
        <Col span={12}>
          <Row justify="start" align="middle">
            <Text strong style={{ width: "4em", minWidth: "4em" }}>
              {" "}
              Search:{" "}
            </Text>
            <Col span={19}>
              <SearchInput
                onChange={searchList}
                placeHolder="Search for service's name, member, phone number, and email"
              />
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

BookingStayTable.displayName = "BookingStayTable";
