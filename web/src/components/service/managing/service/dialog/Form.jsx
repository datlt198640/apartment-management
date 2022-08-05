import { Form, Input, TimePicker, Checkbox, Upload, Button } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import Utils from "utils/Utils";
import FormUtils from "utils/FormUtils";
import SelectInput from "utils/components/ant_form/input/SelectInput";
import { urls, formLabels, emptyRecord } from "../config";
import moment from "moment";

/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

const formName = "ServiceForm";

/**
 * ServiceForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 * @param {Object} props.formRef
 */

const dateFormat = "YYYY/MM/DD";

export default function ServiceForm({ data, onChange }) {
  const [form] = Form.useForm();
  const listGender = [
    {
      label: "Male",
      value: 0,
    },
    {
      label: "Female",
      value: 1,
    },
  ];

  const initialValues = Utils.isEmpty(data) ? emptyRecord : { ...data };
  const id = initialValues.id;

  const dobObj = new Date(initialValues.dob);
  initialValues.dob = moment(dobObj);

  const endPoint = id ? `${urls.crud}${id}` : urls.crud;
  const method = id ? "put" : "post";

  const formAttrs = {
    title: {
      name: "title",
      label: formLabels.title,
      rules: [FormUtils.ruleRequired()],
    },
    description: {
      name: "description",
      label: formLabels.description,
      rules: [FormUtils.ruleRequired()],
    },
    content: {
      name: "content",
      label: formLabels.content,
      rules: [FormUtils.ruleRequired()],
    },
    bookable: {
      name: "bookable",
      label: formLabels.bookable,
      rules: [FormUtils.ruleRequired()],
    },
    hasMenu: {
      name: "has_menu",
      label: formLabels.hasMenu,
      rules: [FormUtils.ruleRequired()],
    },
    type: {
      name: "type",
      label: formLabels.type,
    },
    subserviceType: {
      name: "subservice_type",
      label: formLabels.subserviceType,
    },
    openTime: {
      name: "open_time",
      label: formLabels.openTime,
    },
    closeTime: {
      name: "close_time",
      label: formLabels.closeTime,
    },
    imageUrl: {
      name: "image_url",
      label: formLabels.image,
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
    <Form
      form={form}
      name={formName}
      labelCol={{ span: 4 }}
      wrapperCol={{ span: 20 }}
      initialValues={{ ...initialValues }}
      onFinish={onFinish}
    >
      <Form.Item {...formAttrs.title}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.description}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.content}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.type}>
        <SelectInput options={listGender} />
      </Form.Item>
      <Form.Item {...formAttrs.subserviceType}>
        <SelectInput options={listGender} />
      </Form.Item>
      <Form.Item {...formAttrs.openTime}>
        <TimePicker />
      </Form.Item>
      <Form.Item {...formAttrs.closeTime}>
        <TimePicker />
      </Form.Item>
      <Form.Item {...formAttrs.bookable}>
        <Checkbox />
      </Form.Item>
      <Form.Item {...formAttrs.hasMenu}>
        <Checkbox />
      </Form.Item>
      <Form.Item {...formAttrs.imageUrl}>
        <Upload
          listType="picture"
          className="upload-list-inline"
          multiple
          beforeUpload={() => false}
        >
          <Button icon={<UploadOutlined />}>Upload</Button>
        </Upload>
      </Form.Item>
    </Form>
  );
}

ServiceForm.displayName = formName;
ServiceForm.formName = formName;
