import Utils from "utils/Utils";

const urlMap = {
  base: {
    prefix: "services/service",
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
  subserviceType: "",
};

export const formLabels = {
  title: "Title",
  description: "Description",
  content: "Content",
  bookable: "Bookable",
  hasMenu: "Has Menu",
  type: "Type",
  subserviceType: "Subservice Type",
  openTime: "Open Time",
  closeTime: "Close Time",
  image: "Image",
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
    key: "bookable",
    title: "Bookable",
    dataIndex: "bookable",
    width: 80,
  },
  {
    key: "has_menu",
    title: "Has Menu",
    dataIndex: "has_menu",
    width: 120,
  },
  {
    key: "type",
    title: "Type",
    dataIndex: "type",
    width: 300,
  },
  {
    key: "subservice_type",
    title: "Subservice Type",
    dataIndex: "subservice_type",
    width: 150,
  },
  {
    key: "action",
    title: "",
    fixed: "right",
    width: 90,
  },
];

export const SERVICE_TYPE = [
  // { value: 0, label: "None" },
  { value: 1, label: "STAY" },
  { value: 2, label: "CELEBRATE" },
  { value: 3, label: "ENTERTAIN" },
  { value: 4, label: "DINE" },
  { value: 5, label: "SHOP" },
  { value: 6, label: "RELAX" },
];
