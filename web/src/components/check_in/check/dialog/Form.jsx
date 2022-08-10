import { useRecoilValue } from "recoil";
import React, { useState } from "react";
import {
  Typography,
  Card,
  Row,
  Form,
  Avatar,
  notification,
  Col,
  Skeleton,
} from "antd";
import Utils from "utils/Utils";
import { urls, emptyRecord } from "../config";
import { ArrowRightOutlined } from "@ant-design/icons";
import { listMemberSt } from "../states";
import QrScan from "react-qr-reader";
import moment from "moment";
import FormUtils from "utils/FormUtils";
import styles from "../style.module.css";
// import {}
const formName = "CheckInForm";

/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

/**
 * CheckInForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 *
 */

const { Title } = Typography;
const { Text } = Typography;

export default function CheckInForm({ data, onChange }) {
  const [form] = Form.useForm();
  const [qrMember, setQRMember] = useState(-1);
  const listMember = useRecoilValue(listMemberSt);
  const currentDate = moment().toISOString();

  const initialValues = Utils.isEmpty(data) ? emptyRecord : data;
  const id = initialValues.id;
  const endPoint = id ? `${urls.crud}${id}` : urls.crud;
  const method = id ? "put" : "post";

  const openNotificationError = (type, message) => {
    notification[type]({
      message: message,
    });
  };

  const handleScan = (data) => {
    if (data) {
      const result = listMember.filter((member) => member.uid == data)[0];
      if (!result) {
        openNotificationError("error", "Invalid QR Code !");
      }
      setQRMember(result);
    }
  };

  const CheckIn = () => {
    const params = {
      member: qrMember["id"],
      check_in: Utils.getCurrentTime(),
    };
    FormUtils.submit(endPoint, params, method)
      .then((params) => onChange(params, id))
      .catch((err) => openNotificationError("error", err));
  };

  const handleError = (err) => {
    console.error("err", err);
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Row
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
        }}
      >
        <Col xs={10} sm={10} md={10} lg={10} xl={10} xxl={10}>
          <Form
            form={form}
            name={formName}
            onFinish={CheckIn}
            className={styles.column}
          >
            <QrScan
              delay={300}
              className={styles.qrScan}
              onError={handleError}
              onScan={handleScan}
            />
          </Form>
        </Col>
        <Col xs={4} sm={4} md={4} lg={4} xl={4} xxl={4}>
          <ArrowRightOutlined
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: "30px",
            }}
          />
        </Col>
        <Col
          xs={10}
          sm={10}
          md={10}
          lg={10}
          xl={10}
          xxl={10}
          className={styles.column}
        >
          {qrMember == -1 ? (
            <Skeleton active />
          ) : (
            <Card className={styles.card}>
              <Row justify={"center"} align={"center"}>
                <Avatar src={qrMember?.avatar} className={styles.avatar} />
              </Row>
              <Text
                style={{
                  marginBottom: 0,
                  textAlign: "center",
                  display: "block",
                }}
              >
                {qrMember?.full_name}
              </Text>
              <Row
                style={{
                  width: "100%",
                  display: "block",
                }}
              >
                <Text
                  style={{
                    textAlign: "center",
                    display: "block",
                  }}
                >
                  {qrMember?.membership_type?.title}{" "}
                </Text>
              </Row>
              <Row>
                <Text className={styles.text}>
                  Date of birth: {qrMember?.dob}
                </Text>
              </Row>
              <Row>
                <Text className={styles.text}>
                  {" "}
                  Occupation: {qrMember?.occupation}{" "}
                </Text>
              </Row>
              <Row>
                <Text className={styles.text}>
                  {" "}
                  Address: {qrMember?.address}{" "}
                </Text>
              </Row>
            </Card>
          )}
        </Col>
      </Row>
    </div>
  );
}

CheckInForm.displayName = formName;
CheckInForm.formName = formName;
