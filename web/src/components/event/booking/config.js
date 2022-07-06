import Utils from "utils/Utils";

const urlMap = {
    base: {
        prefix: "event/event/booking",
        endpoints: {
            crud: ""
        }
    }
};
export const urls = Utils.prefixMapValues(urlMap.base);

const headingTxt = "Booking Event";
export const messages = {
    heading: headingTxt,
    deleteOne: `Do you want to delete this ${headingTxt.toLowerCase()}?`,
    deleteMultiple: `Do you want to delete these ${headingTxt.toLowerCase()}s?`,
};

export const emptyRecord = {
    id: 0,
    event: "",
    member: "",
    memberName: "",
    phoneNumber: "",
    email: "",
};

export const labels = {
    id: "ID",
    event: "Event",
    member: "Member",
    memberName: "Member Name",
    phoneNumber: "Phone number",
    email: "Email",
};
