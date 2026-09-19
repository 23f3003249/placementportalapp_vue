// Axios Configuration
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000",
  withCredentials: true,
});

api.interceptors.response.use(
  (response) => response,

  (error) => {
    if (!error.response) {
      return Promise.reject(error);
    }

    const status = error.response.status;
    const message = error.response.data?.message || "";

    // No valid login/session
    if (status === 401) {
      if (window.location.pathname !== "/login") {
        alert(message || "Authentication required");
        window.location.replace("/login");
      }

      return Promise.reject(error);
    }

    // Blocked/deactivated account only
    if (
      status === 403 &&
      (message === "Account blocked" ||
        message === "Your account has been blocked by admin" ||
        message === "Account deactivated")
    ) {
      alert(message);

      if (window.location.pathname !== "/login") {
        window.location.replace("/login");
      }

      return Promise.reject(error);
    }

    return Promise.reject(error);
  },
);

export default api;
