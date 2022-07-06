import Utils from "utils/Utils";

const urlMap = {
  base: {
    prefix: "account/member/booking-service",
    endpoints: {
      crud: "",
    },
  },
};
export const urls = Utils.prefixMapValues(urlMap.base);

const headingTxt = "Booking Celebrate";
export const messages = {
  heading: headingTxt,
  deleteOne: `Do you want to delete this ${headingTxt.toLowerCase()}?`,
  deleteMultiple: `Do you want to delete these ${headingTxt.toLowerCase()}s?`,
};

export const emptyRecord = {
  id: 0,
  service: "",
  member: "",
  member_name: "",
  phone_number: "",
  email: "",
  date: "",
  time: "",
  participants: "",
};

export const labels = {
  id: "ID",
  service: "Service",
  member: "Member",
  memberName: "Booking Name",
  phoneNumber: "Phone number",
  email: "Email",
  date: "Date",
  time: "Time",
  participants: "Participants",
};