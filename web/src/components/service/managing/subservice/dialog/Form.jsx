import { Form, Input, InputNumber, TimePicker } from "antd";
import Utils from "utils/Utils";
import FormUtils from "utils/FormUtils";
import SelectInput from "utils/components/ant_form/input/SelectInput";
import { urls, formLabels, emptyRecord } from "../config";
import moment from "moment";
import { useRecoilValue } from "recoil";
import { listSubserviceCategorySt } from "../states";
/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

const formName = "SubserviceForm";

/**
 * SubserviceForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 * @param {Object} props.formRef
 */

const dateFormat = "HH:mm:ss";

export default function SubserviceForm({ data, onChange }) {
  const [form] = Form.useForm();
  const listSubserviceCategory = useRecoilValue(listSubserviceCategorySt);

  const initialValues = Utils.isEmpty(data) ? emptyRecord : { ...data };
  const id = initialValues.id;

  console.log("initialValues", initialValues);

  const openTimeObj = new Date(initialValues.open_time);
  initialValues.open_time = moment(openTimeObj);

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
    price: {
      name: "price",
      label: formLabels.price,
      rules: [FormUtils.ruleRequired()],
    },
    openTime: {
      name: "open_time",
      label: formLabels.openTime,
      rules: [FormUtils.ruleRequired()],
    },
    duration: {
      name: "duration",
      label: formLabels.duration,
    },
    subserviceCategory: {
      name: "subservice_category",
      label: formLabels.subserviceCategory,
    },
  };

  const onFinish = (payload) => {
    payload.open_time = moment(payload.open_time).format("HH:mm");
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
      <Form.Item {...formAttrs.price}>
        <InputNumber />
      </Form.Item>
      <Form.Item {...formAttrs.openTime}>
        <TimePicker format={dateFormat} />
      </Form.Item>
      <Form.Item {...formAttrs.duration}>
        <InputNumber />
      </Form.Item>
      <Form.Item {...formAttrs.subserviceCategory}>
        <SelectInput options={listSubserviceCategory} />
      </Form.Item>
    </Form>
  );
}

SubserviceForm.displayName = formName;
SubserviceForm.formName = formName;
