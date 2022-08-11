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

const headingTxt = "Subservice ";
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
  price: "",
  openTime: "",
  duration: "",
  subserviceCategory: "",
};

export const formLabels = {
  title: "Title",
  description: "Description",
  content: "Content",
  price: "Price",
  openTime: "Open Time",
  duration: "Duration",
  subserviceCategory: "Subservice Category",
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
    key: "price",
    title: "Price",
    dataIndex: "price",
    width: 120,
  },
  {
    key: "open_time",
    title: "Open Time",
    dataIndex: "open_time",
    width: 300,
  },
  {
    key: "duration",
    title: "Duration",
    dataIndex: "duration",
    width: 150,
  },
  {
    key: "subservice_category",
    title: "Subservice Category",
    dataIndex: "subservice_category",
    width: 100,
  },
  {
    key: "action",
    title: "",
    fixed: "right",
    width: 90,
  },
];
