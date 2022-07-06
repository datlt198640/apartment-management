import { Form, Input } from "antd";
import SelectInput from "utils/components/ant_form/input/SelectInput";
import Utils from "utils/Utils";
import FormUtils from "utils/FormUtils";
import { urls, labels, emptyRecord } from "../config";
import {useRecoilValue } from "recoil";
import {listMemberEventSt, listEventSt} from "../states";

const formName = "BookingForm";

/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

/**
 * BookingForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 */
export default function BookingForm({ data, onChange }) {
    const [form] = Form.useForm();
    const initialValues = Utils.isEmpty(data) ? emptyRecord : data;
    const id = initialValues.id;

    const endPoint = id ? `${urls.crud}${id}` : urls.crud;
    const method = id ? "put" : "post";

    // const listMemberEvent = useRecoilValue(listMemberEventSt)
    const listEvent = useRecoilValue(listEventSt)

    const formAttrs = {
        event: {
            name: "event",
            label: labels.event,
            rules: [FormUtils.ruleRequired()]
        },
        memberName: {
            name: "member_name",
            label: labels.memberName,
        },
        phoneNumber: {
            name: "phone_number",
            label: labels.phoneNumber
        },
        email: {
            name: "email",
            label: labels.email
        },
    };

    return (
        <Form
            form={form}
            name={formName}
            labelCol={{ span: 6 }}
            wrapperCol={{ span: 18 }}
            initialValues={{ ...initialValues }}
            onFinish={(payload) =>
                FormUtils.submit(endPoint, payload, method)
                    .then((data) => onChange(data, id))
                    .catch(FormUtils.setFormErrors(form))
            }
        >
            <Form.Item {...formAttrs.event}>
                <SelectInput options={listEvent}  />
            </Form.Item>
            {/* <Form.Item {...formAttrs.member}>
                <SelectInput options={listMemberEvent}  />
            </Form.Item> */}
            <Form.Item {...formAttrs.memberName}>
                <Input />
            </Form.Item>

            <Form.Item {...formAttrs.phoneNumber}>
                <Input />
            </Form.Item>
            
            <Form.Item {...formAttrs.email}>
                <Input />
            </Form.Item>
        </Form>
    );
}

BookingForm.displayName = formName;
BookingForm.formName = formName;
