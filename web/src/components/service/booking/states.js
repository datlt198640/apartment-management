import { atom } from "recoil";

export const listServiceSt = atom({
  key: "listService",
  default: [],
});

export const listMemberSt = atom({
  key: "listMember",
  default: [],
});

export const listMembershipTypeSt = atom({
  key: "listMembershipType",
  default: [],
});
