import Utils from "utils/Utils";


const urlMap = {
    base: {
      prefix: "account/member",
      endpoints: {
        crud: "",
      },
    },
};

export const urls = Utils.prefixMapValues(urlMap.base);

const headingTxt = "Member ";
export const messages = {
    heading: headingTxt,
    deleteOne: `Do you want to delete this ${headingTxt.toLowerCase()}?`,
    deleteMultiple: `Do you want to delete these ${headingTxt.toLowerCase()} ?`
};

export const emptyRecord = {
    id: 0,
    phone_number: "",
    email: "",
    password: "",
    fullName: "",
    groups: "",
    gender: "",
    dob: "",
    occupation: "",
    address: "",
    member_remote_id: "",
};

export const formLabels = {
    phone_number: "Phone number",
    email: "Email",
    password: "Password",
    fullName: "Full name",
    groups: "Group",
    gender: "Gender",
    dob: "Date of birth",
    occupation: "Occupation",
    address: "Address",
    memberUID: "Member ID",
};

export const columns = [
    {
        key: "full_name",
        title: "Full name",
        dataIndex: "full_name"
    },
    {
        key: "phone_number",
        title: "Phone number",
        dataIndex: "phone_number"
    },
    {
        key: "email",
        title: "Email",
        dataIndex: "email"
    },
    {
        key: "gender",
        title: "Gender",
        dataIndex: "gender",
        width: 100
    },
    {
        key: "dob",
        title: "Date of birth",
        dataIndex: "dob",
        width: 140
    },
    {
        key: "address",
        title: "Address",
        dataIndex: "address"
    },
    {
        key: "occupation",
        title: "Occupation",
        dataIndex: "occupation"
    },
    {
        key: "membership_type",
        title: "Type",
        dataIndex: "membership_type",
        width: 100
    },
    {
        key: "action",
        title: "",
        fixed: "right",
        width: 90
    }
];
