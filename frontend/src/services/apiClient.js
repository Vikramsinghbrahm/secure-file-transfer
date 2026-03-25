import axios from "axios";

const storageKeys = {
  token: "vaultflow.token",
  user: "vaultflow.user",
};

function normalizeBaseUrl(baseUrl) {
  return baseUrl.replace(/\/+$/, "");
}

function isPrivateNetworkHost(hostname) {
  return (
    ["localhost", "127.0.0.1"].includes(hostname) ||
    /^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(hostname) ||
    /^192\.168\.\d{1,3}\.\d{1,3}$/.test(hostname) ||
    /^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$/.test(hostname)
  );
}

function resolveApiBaseUrl() {
  if (import.meta.env.VITE_API_BASE_URL) {
    return normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL);
  }

  if (typeof window === "undefined") {
    return "/api/v1";
  }

  const { hostname, origin, port, protocol } = window.location;
  const isLocalDevHost = isPrivateNetworkHost(hostname);

  if (isLocalDevHost && port !== "5001") {
    return `${protocol}//${hostname}:5001/api/v1`;
  }

  return `${origin}/api/v1`;
}

const apiClient = axios.create({
  baseURL: resolveApiBaseUrl(),
  timeout: 15000,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(storageKeys.token);

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

function unwrapError(error) {
  return (
    error?.response?.data?.message ||
    error?.message ||
    "The request could not be completed."
  );
}

export { apiClient, storageKeys, unwrapError };
