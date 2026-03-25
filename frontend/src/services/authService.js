import { apiClient } from "./apiClient";

async function register(credentials) {
  const response = await apiClient.post("/auth/register", credentials);
  return response.data;
}

async function login(credentials) {
  const response = await apiClient.post("/auth/login", credentials);
  return response.data;
}

export { login, register };
