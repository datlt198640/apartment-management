import { Form, Input } from "antd";
import Utils from "utils/Utils";
import FormUtils from "utils/FormUtils";
import SelectInput from "utils/components/ant_form/input/SelectInput";
import { urls, formLabels, emptyRecord } from "../config";
import moment from "moment";
import { useRecoilValue } from "recoil";
import { listSubserviceTypeSt } from "../states";


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
  const lstSubserviceType = useRecoilValue(listSubserviceTypeSt)

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
    subserviceType: {
      name: "subservice_type",
      label: formLabels.subserviceType,
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
      <Form.Item {...formAttrs.description}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.content}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.subserviceType}>
        <SelectInput options={lstSubserviceType} />
      </Form.Item>
    </Form>
  );
}

ServiceForm.displayName = formName;
ServiceForm.formName = formName;
