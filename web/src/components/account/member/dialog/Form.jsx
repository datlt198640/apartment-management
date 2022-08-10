import { Form, Input, DatePicker } from "antd";
import Utils from "utils/Utils";
import FormUtils from "utils/FormUtils";
import SelectInput from "utils/components/ant_form/input/SelectInput";
import { urls, formLabels, emptyRecord } from "../config";
import moment from "moment";
import { useRecoilValue } from "recoil";
import { listMembershipTypeSt } from "../states";
/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

const formName = "MemberForm";

/**
 * MemberForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 * @param {Object} props.formRef
 */

const dateFormat = "DD/MM/YYYY";

export default function MemberForm({ data, onChange }) {
  const [form] = Form.useForm();
  const listMembershipType = useRecoilValue(listMembershipTypeSt);
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

  const registerDateObj = new Date(initialValues.register_date);
  initialValues.register_date = moment(registerDateObj);

  const expiryObj = new Date(initialValues.expire_date);
  initialValues.expire_date = moment(expiryObj);

  const endPoint = id ? `${urls.crud}${id}` : urls.crud;
  const method = id ? "put" : "post";

  const formAttrs = {
    phoneNumber: {
      name: "phone_number",
      label: formLabels.phoneNumber,
    },
    email: {
      name: "email",
      label: formLabels.email,
    },
    fullName: {
      name: "full_name",
      label: formLabels.fullName,
      rules: [FormUtils.ruleRequired()],
    },
    password: {
      name: "password",
      label: formLabels.password,
      rules: [FormUtils.ruleRequired()],
    },
    gender: {
      name: "gender",
      label: formLabels.gender,
      rules: [FormUtils.ruleRequired()],
    },
    dob: {
      name: "dob",
      label: formLabels.dob,
    },
    occupation: {
      name: "occupation",
      label: formLabels.occupation,
    },
    address: {
      name: "address",
      label: formLabels.address,
    },
    registerDate: {
      name: "register_date",
      label: formLabels.register_date,
    },
    expireDate: {
      name: "expire_date",
      label: formLabels.expire_date,
    },
    membershipType: {
      name: "membership_type",
      label: formLabels.membership_type,
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
      <Form.Item {...formAttrs.email}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.phoneNumber}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.fullName}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.dob}>
        <DatePicker format={dateFormat} />
      </Form.Item>
      <Form.Item {...formAttrs.occupation}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.address}>
        <Input />
      </Form.Item>
      <Form.Item {...formAttrs.gender}>
        <SelectInput options={listGender} />
      </Form.Item>
      {!initialValues.id && (
        <Form.Item {...formAttrs.password}>
          <Input.Password />
        </Form.Item>
      )}
      <Form.Item {...formAttrs.membershipType}>
        <SelectInput options={listMembershipType} />
      </Form.Item>
      <Form.Item {...formAttrs.registerDate}>
        <DatePicker format={dateFormat} />
      </Form.Item>
      <Form.Item {...formAttrs.expireDate}>
        <DatePicker format={dateFormat} />
      </Form.Item>
    </Form>
  );
}

MemberForm.displayName = formName;
MemberForm.formName = formName;
