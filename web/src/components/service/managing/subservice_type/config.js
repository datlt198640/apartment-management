import Utils from "utils/Utils";

const urlMap = {
  base: {
    prefix: "services/subservice/type",
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
};

export const formLabels = {
  title: "Title",
};

export const columns = [
  {
    key: "title",
    title: "Title",
    dataIndex: "title",
    width: 150,
  },
  {
    key: "action",
    title: "",
    fixed: "right",
    width: 90,
  },
];
