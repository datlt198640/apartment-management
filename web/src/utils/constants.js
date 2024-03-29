import { createBrowserHistory } from "history";

export const ENV = import.meta.env;

export const APP_NAMESPACE = ENV.VITE_NAMESPACE;
export const DEV_MODE = parseInt(ENV.VITE_DEV_MODE);

export const PROTOCOL = window.location.protocol + "//";
export const DOMAIN = window.location.host;
export const API_PREFIX = "/api/v1/";

export const LOCAL_STORAGE_PREFIX = APP_NAMESPACE;

export const History = createBrowserHistory({});
export const LOGO_TEXT = ENV.VITE_LOGO_TEXT || "APTM";
export const HR_DEPUTY = ENV.VITE_HR_DEPUTY || "Ban Phát triển Nhân lực";
