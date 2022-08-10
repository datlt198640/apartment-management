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
  deleteMultiple: `Do you want to delete these ${headingTxt.toLowerCase()} ?`,
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
  register_date: "",
  expire_date: "",
  membership_type: "",
};

export const formLabels = {
  phoneNumber: "Phone number",
  email: "Email",
  password: "Password",
  fullName: "Full name",
  groups: "Group",
  gender: "Gender",
  dob: "Date of birth",
  occupation: "Occupation",
  address: "Address",
  memberUID: "Member ID",
  register_date: "Register Date",
  expire_date: "Expired Date",
  membership_type: "Membership Type",
};

export const columns = [
  {
    key: "full_name",
    title: "Full name",
    dataIndex: "full_name",
    width: 150,
  },
  {
    key: "phone_number",
    title: "Phone number",
    dataIndex: "phone_number",
    width: 150,
  },
  {
    key: "email",
    title: "Email",
    dataIndex: "email",
    width: 200,
  },
  {
    key: "gender",
    title: "Gender",
    dataIndex: "gender",
    width: 80,
  },
  {
    key: "dob",
    title: "Date of birth",
    dataIndex: "dob",
    width: 120,
  },
  {
    key: "address",
    title: "Address",
    dataIndex: "address",
    width: 300,
  },
  {
    key: "occupation",
    title: "Occupation",
    dataIndex: "occupation",
    width: 150,
  },
  {
    key: "membership_type",
    title: "MembershipType",
    dataIndex: "membership_type",
    width: 100,
  },
  {
    key: "register_date",
    title: "Register Date",
    dataIndex: "register_date",
    width: 100,
  },
  {
    key: "expire_date",
    title: "Expired Date",
    dataIndex: "expire_date",
    width: 100,
  },
  {
    key: "action",
    title: "",
    fixed: "right",
    width: 90,
  },
];
