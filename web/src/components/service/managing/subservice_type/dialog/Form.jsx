import { Form, Input, DatePicker } from "antd";
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

const formName = "SubserviceTypeForm";

/**
 * SubserviceTypeForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 * @param {Object} props.formRef
 */

const dateFormat = "YYYY/MM/DD";

export default function SubserviceTypeForm({ data, onChange }) {
  const [form] = Form.useForm();

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
  };

  return (
    <Form
      form={form}
      name={formName}
      labelCol={{ span: 4 }}
      wrapperCol={{ span: 20 }}
      initialValues={{ ...initialValues }}
      onFinish={(payload) =>
        FormUtils.submit(endPoint, payload, method)
          .then((data) => onChange(data, id))
          .catch(FormUtils.setFormErrors(form))
      }
    >
      <Form.Item {...formAttrs.title}>
        <Input />
      </Form.Item>
    </Form>
  );
}

SubserviceTypeForm.displayName = formName;
SubserviceTypeForm.formName = formName;
