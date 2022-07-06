import { useState, useEffect } from "react";
import { Modal } from "antd";
import Utils from "utils/Utils";
import Form from "./Form";
import { urls, emptyRecord, messages } from "../config";

export class Service {
    static get toggleEvent() {
        return "TOGGLE_CHECK_IN_DIALOG";
    }

    static toggle(open = true, id = 0) {
        Utils.event.dispatch(Service.toggleEvent, { open, id });
    }
}

/**
 * CheckInDialog.
 *
 * @param {Object} props
 * @param {function} props.onChange - (data: Dict, id: number) => void
 */
export default function CheckInDialog({ onChange }) {
    const [data, setData] = useState({ ...emptyRecord });
    const [open, setOpen] = useState(false);
    const [id, setId] = useState(0);

    const handleToggle = ({ detail: { open, id } }) => {
        if (!open) return setOpen(false);
        setId(id);
        if (id) {
            Utils.toggleGlobalLoading();
            Utils.apiCall(`${urls.crud}${id}`)
                .then((resp) => {
                    setData(resp.data);
                    setOpen(true);
                })
                .finally(() => Utils.toggleGlobalLoading(false));
        } else {
            setData({ ...emptyRecord });
            setOpen(true);
        }
    };

    useEffect(() => {
        Utils.event.listen(Service.toggleEvent, handleToggle);
        return () => {
            Utils.event.remove(Service.toggleEvent, handleToggle);
        };
    }, []);
    return (
        <Modal
            keyboard={false}
            maskClosable={false}
            destroyOnClose
            visible={open}
            okButtonProps={{ form: Form.formName, key: "submit", htmlType: "submit" }}
            okText="Check in "
            onCancel={() => Service.toggle(false)}
            cancelText="Thoát"
            title={Utils.getDialogTitle(id, messages)}
            width="79%"
        >
            <Form
                data={data}
                onChange={(data, id) => {
                    setOpen(false);
                    onChange(data, id);
                }}
            />
        </Modal>
    );
}

CheckInDialog.displayName = "CheckInDialog";
CheckInDialog.toggle = Service.toggle;
