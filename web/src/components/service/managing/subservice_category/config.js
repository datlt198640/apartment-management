import Utils from "utils/Utils";

const urlMap = {
  base: {
    prefix: "services/subservice/category",
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
  subserviceType: "",
};

export const formLabels = {
  title: "Title",
  description: "Description",
  content: "Content",
  subserviceType: "Subservice Type",
};

export const columns = [
  {
    key: "title",
    title: "Title",
    dataIndex: "title",
    width: 150,
  },
  {
    key: "description",
    title: "Description",
    dataIndex: "description",
    width: 150,
  },
  {
    key: "content",
    title: "Content",
    dataIndex: "content",
    width: 200,
  },
  {
    key: "subservice_type",
    title: "Subservice Type",
    dataIndex: "subservice_type",
    width: 100,
  },
  {
    key: "action",
    title: "",
    fixed: "right",
    width: 90,
  },
];
