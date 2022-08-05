import Utils from "utils/Utils";

const urlMap = {
  base: {
    prefix: "services/subservice",
    endpoints: {
      crud: "",
    },
  },
};

export const urls = Utils.prefixMapValues(urlMap.base);

const headingTxt = "Service ";
export const messages = {
  heading: headingTxt,
  deleteOne: `Do you want to delete this ${headingTxt.toLowerCase()}?`,
  deleteMultiple: `Do you want to delete these ${headingTxt.toLowerCase()} ?`,
};

export const emptyRecord = {
  id: 0,
  title: "",
  description: "",
  content: "",
  bookable: "",
  hasMenu: "",
  type: "",
  subserviceTitle: "",
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
    title: "Type",
    dataIndex: "membership_type",
    width: 100,
  },
  {
    key: "action",
    title: "",
    fixed: "right",
    width: 90,
  },
];
