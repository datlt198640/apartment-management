import Utils from "utils/Utils";

const urlMap = {
  base: {
    prefix: "account/check-in",
    endpoints: {
      crud: "",
    },
  },
};
export const urls = Utils.prefixMapValues(urlMap.base);

const headingTxt = "Check In";
export const messages = {
  heading: headingTxt,
  deleteOne: `Do you want to delete this ${headingTxt.toLowerCase()}?`,
  checkOut: `Do you want to check out this ${headingTxt.toLowerCase()}?`,
  deleteMultiple: `Do you want to delete these ${headingTxt.toLowerCase()}s?`,
};

export const emptyRecord = {
  id: 0,
  member: "",
  check_in: "1111-11-11 00:00:00 ",
  check_out: "1111-11-11 00:00:00",
};

export const labels = {
  id: "id",
  member: "Member",
  memberEmail: "Email",
  memberPhoneNumber: "Phone Number",
  check_in: "Check In",
  check_out: "Check Out",
};
