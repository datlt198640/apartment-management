import React from "react";
import { Form, Input, DatePicker, Upload, Button, Image, Space } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import Utils from "utils/Utils";
import FormUtils from "utils/FormUtils";
import { urls, labels, emptyRecord } from "../config";
import moment from "moment";
// import {}
const formName = "EventForm";
const dateFormat = "YYYY-MM-DD HH:mm";

/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

/**
 * EventForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 */

const { TextArea } = Input;
const { RangePicker } = DatePicker;

export default function EventForm({ data, onChange }) {
  console.log("data", data.image_url);
  console.log("location", window.location.hostname);

  const [form] = Form.useForm();

  const initialValues = Utils.isEmpty(data) ? emptyRecord : data;
  const id = initialValues.id;
  const endPoint = id ? `${urls.crud}${id}` : urls.crud;
  const method = id ? "put" : "post";

  const formAttrs = {
    title: {
      name: "title",
      label: labels.title,
      rules: [FormUtils.ruleRequired()],
    },
    description: {
      name: "description",
      label: labels.description,
    },
    content: {
      name: "content",
      label: labels.content,
    },
    startTime: {
      name: "start_time",
      label: labels.start_time,
    },
    end_time: {
      name: "end_time",
      label: labels.end_time,
    },
    time: {
      name: "time",
      label: labels.time,
      rules: [FormUtils.ruleRequired()],
    },
    imageUrl: {
      name: "image_url",
      label: labels.image_url,
    },
    Images: {
      name: "Images",
      label: "Old Images",
    },
  };

  const onFinish = (payload) => {
    let listImg = [];
    payload?.image_url?.fileList?.map((file) => {
      listImg.push(file.originFileObj);
    });
    payload.image_url = listImg;
    payload.start_time = moment(payload.time[0]).format("YYYY-MM-DD HH:mm");
    payload.end_time = moment(payload.time[1]).format("YYYY-MM-DD HH:mm");
    Utils.getFormDataPayload();
    FormUtils.submit(endPoint, payload, method)
      .then((data) => onChange(data, id))
      .catch(FormUtils.setFormErrors(form));
  };

  return (
    <Form form={form} name={formName} initialValues={{ ...initialValues }} onFinish={onFinish} layout="vertical">
      <Form.Item {...formAttrs.title}>
        <Input autoFocus />
      </Form.Item>

      <Form.Item {...formAttrs.description}>
        <TextArea showCount maxLength={225} />
      </Form.Item>

      <Form.Item {...formAttrs.content}>
        <TextArea showCount maxLength={1000} />
      </Form.Item>

      <Form.Item {...formAttrs.time}>
        <RangePicker
          defaultValue={
            initialValues
              ? [moment(initialValues.start_time, dateFormat), moment(initialValues.end_time, dateFormat)]
              : []
          }
          showTime
          format="YYYY/MM/DD HH:mm"
        />
      </Form.Item>
      <Form.Item {...formAttrs.Images}>
        {initialValues?.image_url?.map((image) => {
          return <Space> <Image style = {{minWidth:"100px", maxWidth:"100px", minHeight:"100px", maxHeight:"100px"}} src={image} preview={false} /></Space>
        })}
      </Form.Item>
      <Form.Item {...formAttrs.imageUrl}>
        <Upload listType="picture" className="upload-list-inline" multiple beforeUpload={() => false}>
          <Button icon={<UploadOutlined />}>Upload</Button>
        </Upload>
      </Form.Item>
    </Form>
  );
}

EventForm.displayName = formName;
EventForm.formName = formName;
