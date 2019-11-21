import ky from "ky";
import authHeader from "./auth-header";

export default ky.extend({
  hooks: {
    beforeRequest: [
      (url, request) => {
        const headers = { ...authHeader() };
        Object.keys(headers).forEach(key => {
          request.headers.set(key, headers[key]);
        });
      }
    ]
  },
  prefixUrl: "//0.0.0.0:8001"
});
