import { Form, Input, TimePicker, Checkbox, Upload, Button } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import Utils from "utils/Utils";
import FormUtils from "utils/FormUtils";
import SelectInput from "utils/components/ant_form/input/SelectInput";
import { urls, formLabels, emptyRecord, SERVICE_TYPE } from "../config";
import moment from "moment";
import { useRecoilValue } from "recoil";
import { listSubserviceTypeSt, listSubserviceCategorySt } from "../states";
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

const dateFormat = "HH:mm";

export default function ServiceForm({ data, onChange }) {
  const [form] = Form.useForm();
  const listSubserviceType = useRecoilValue(listSubserviceTypeSt);
  const listSubserviceCategory = useRecoilValue(listSubserviceCategorySt);

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
    },
    bookable: {
      name: "bookable",
      label: formLabels.bookable,
    },
    hasMenu: {
      name: "has_menu",
      label: formLabels.hasMenu,
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
    console.log("payload", payload);
    let listImg = [];
    payload?.image_url?.fileList?.map((file) => {
      listImg.push(file.originFileObj);
    });
    payload.image_url = listImg;
    payload.open_time = moment(payload.open_time).format("HH:mm");
    payload.close_time = moment(payload.close_time).format("HH:mm");
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
        <SelectInput options={SERVICE_TYPE} />
      </Form.Item>
      <Form.Item {...formAttrs.subserviceType}>
        <SelectInput options={listSubserviceType} />
      </Form.Item>
      <Form.Item {...formAttrs.openTime}>
        <TimePicker format={dateFormat} />
      </Form.Item>
      <Form.Item {...formAttrs.closeTime}>
        <TimePicker format={dateFormat} />
      </Form.Item>
      {/* <Form.Item {...formAttrs.bookable}>
        <Checkbox />
      </Form.Item>
      <Form.Item {...formAttrs.hasMenu}>
        <Checkbox />
      </Form.Item> */}
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
