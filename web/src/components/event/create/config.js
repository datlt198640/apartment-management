import Utils from "utils/Utils";

const urlMap = {
  base: {
    prefix: "/event/event",
    endpoints: {
      crud: "",
    },
  },
};
export const urls = Utils.prefixMapValues(urlMap.base);

const headingTxt = "Event";
export const messages = {
  heading: headingTxt,
  deleteOne: `Do you want to delete this ${headingTxt.toLowerCase()}`,
  deleteMultiple: `Do you want to delete these ${headingTxt.toLowerCase()}`,
};

export const emptyRecord = {
  id: 0,
  title: "",
  description: "",
  content: "",
  start_time: "",
  end_time: "",
  time: "",
  image_url: [],
};

export const labels = {
  id: "id",
  title: "Tile",
  description: "Description",
  content: "Content",
  start_time: "Start time",
  end_time: "End time ",
  time: "Date time ",
};
