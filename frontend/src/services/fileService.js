import { apiClient } from "./apiClient";

async function fetchFiles() {
  const response = await apiClient.get("/files");
  return response.data;
}

async function fetchDashboard() {
  const response = await apiClient.get("/dashboard");
  return response.data;
}

async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post("/files", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

async function deleteFile(fileId) {
  const response = await apiClient.delete(`/files/${fileId}`);
  return response.data;
}

async function createShareLink(fileId, options = {}) {
  const response = await apiClient.post(`/files/${fileId}/shares`, options);
  return response.data;
}

async function revokeShareLink(shareLinkId) {
  const response = await apiClient.delete(`/shares/${shareLinkId}`);
  return response.data;
}

async function downloadFile(fileId, fallbackName) {
  const response = await apiClient.get(`/files/${fileId}/download`, {
    responseType: "blob",
  });
  const blobUrl = window.URL.createObjectURL(response.data);
  const anchor = document.createElement("a");

  anchor.href = blobUrl;
  anchor.download = getFilename(response.headers["content-disposition"], fallbackName);
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.URL.revokeObjectURL(blobUrl);

  return response.data;
}

function getFilename(contentDisposition, fallbackName) {
  if (!contentDisposition) {
    return fallbackName;
  }

  const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i);
  if (utf8Match?.[1]) {
    return decodeURIComponent(utf8Match[1]);
  }

  const plainMatch = contentDisposition.match(/filename="([^"]+)"/i);
  return plainMatch?.[1] || fallbackName;
}

export {
  createShareLink,
  deleteFile,
  downloadFile,
  fetchDashboard,
  fetchFiles,
  revokeShareLink,
  uploadFile,
};
