import { computed, onMounted, reactive } from "vue";

import { login, register } from "../services/authService";
import {
  createShareLink,
  deleteFile,
  downloadFile,
  fetchDashboard,
  fetchFiles,
  revokeShareLink,
  uploadFile,
} from "../services/fileService";
import { storageKeys, unwrapError } from "../services/apiClient";

function defaultDashboard() {
  return {
    metrics: {
      totalFiles: 0,
      storageBytes: 0,
      downloadCount: 0,
      activeShares: 0,
    },
    recentFiles: [],
    activity: [],
  };
}

function loadUser() {
  const serializedUser = localStorage.getItem(storageKeys.user);

  if (!serializedUser) {
    return null;
  }

  try {
    return JSON.parse(serializedUser);
  } catch (_error) {
    localStorage.removeItem(storageKeys.user);
    return null;
  }
}

export function useTransferWorkspace() {
  const state = reactive({
    authMode: "login",
    username: "",
    password: "",
    token: localStorage.getItem(storageKeys.token),
    user: loadUser(),
    files: [],
    dashboard: defaultDashboard(),
    notice: "",
    error: "",
    latestShareLink: null,
    isAuthenticating: false,
    isRefreshing: false,
    isUploading: false,
    activeDownloadId: null,
    activeDeleteId: null,
    activeShareFileId: null,
    activeRevokeShareId: null,
  });

  const isAuthenticated = computed(() => Boolean(state.token && state.user));
  const metrics = computed(() => state.dashboard.metrics);

  onMounted(() => {
    if (isAuthenticated.value) {
      refreshWorkspace();
    }
  });

  async function submitAuth() {
    state.error = "";
    state.notice = "";
    state.isAuthenticating = true;

    try {
      const payload = {
        username: state.username,
        password: state.password,
      };
      const response =
        state.authMode === "register"
          ? await register(payload)
          : await login(payload);

      persistSession(response.data);
      state.password = "";
      state.notice =
        state.authMode === "register"
          ? "Account provisioned and signed in."
          : "Signed in to the transfer workspace.";

      await refreshWorkspace();
    } catch (error) {
      state.error = unwrapError(error);
    } finally {
      state.isAuthenticating = false;
    }
  }

  async function refreshWorkspace() {
    if (!isAuthenticated.value) {
      return;
    }

    state.error = "";
    state.isRefreshing = true;

    try {
      const [filesResponse, dashboardResponse] = await Promise.all([
        fetchFiles(),
        fetchDashboard(),
      ]);

      state.files = filesResponse.data.files;
      state.dashboard = dashboardResponse.data;
    } catch (error) {
      handleRequestError(error);
    } finally {
      state.isRefreshing = false;
    }
  }

  async function uploadSelectedFile(file) {
    if (!file) {
      state.error = "Choose a file before uploading.";
      return;
    }

    state.error = "";
    state.notice = "";
    state.isUploading = true;

    try {
      const response = await uploadFile(file);
      state.notice = response.message;
      await refreshWorkspace();
    } catch (error) {
      handleRequestError(error);
    } finally {
      state.isUploading = false;
    }
  }

  async function downloadSelectedFile(file) {
    state.error = "";
    state.notice = "";
    state.activeDownloadId = file.id;

    try {
      await downloadFile(file.id, file.name);
      state.notice = `Downloaded ${file.name}.`;
      await refreshWorkspace();
    } catch (error) {
      handleRequestError(error);
    } finally {
      state.activeDownloadId = null;
    }
  }

  async function deleteSelectedFile(file) {
    if (!window.confirm(`Delete ${file.name}? This removes it from your workspace.`)) {
      return;
    }

    state.error = "";
    state.notice = "";
    state.activeDeleteId = file.id;

    try {
      const response = await deleteFile(file.id);
      if (state.latestShareLink?.fileId === file.id) {
        state.latestShareLink = null;
      }
      state.notice = response.message;
      await refreshWorkspace();
    } catch (error) {
      handleRequestError(error);
    } finally {
      state.activeDeleteId = null;
    }
  }

  async function createExpiringShareLink(file) {
    state.error = "";
    state.notice = "";
    state.activeShareFileId = file.id;

    try {
      const response = await createShareLink(file.id, {
        expiresInMinutes: 15,
        maxDownloads: 1,
      });
      state.latestShareLink = {
        ...response.data.shareLink,
        fileId: file.id,
        fileName: file.name,
      };
      state.notice =
        "Expiring share link generated. Copy it now because the full URL is only returned once.";
      await refreshWorkspace();
    } catch (error) {
      handleRequestError(error);
    } finally {
      state.activeShareFileId = null;
    }
  }

  async function revokeExpiringShareLink(shareLink) {
    if (!window.confirm("Revoke this external share link?")) {
      return;
    }

    state.error = "";
    state.notice = "";
    state.activeRevokeShareId = shareLink.id;

    try {
      const response = await revokeShareLink(shareLink.id);
      if (state.latestShareLink?.id === shareLink.id) {
        state.latestShareLink = null;
      }
      state.notice = response.message;
      await refreshWorkspace();
    } catch (error) {
      handleRequestError(error);
    } finally {
      state.activeRevokeShareId = null;
    }
  }

  async function copyLatestShareLink() {
    if (!state.latestShareLink?.shareUrl) {
      return;
    }

    try {
      await navigator.clipboard.writeText(state.latestShareLink.shareUrl);
      state.notice = "Share link copied to clipboard.";
    } catch (_error) {
      state.error =
        "Clipboard access failed. Copy the URL manually from the share panel.";
    }
  }

  function setAuthMode(mode) {
    state.authMode = mode;
    state.error = "";
    state.notice = "";
  }

  function logout() {
    localStorage.removeItem(storageKeys.token);
    localStorage.removeItem(storageKeys.user);

    state.token = null;
    state.user = null;
    state.password = "";
    state.files = [];
    state.dashboard = defaultDashboard();
    state.latestShareLink = null;
    state.activeDownloadId = null;
    state.activeDeleteId = null;
    state.activeShareFileId = null;
    state.activeRevokeShareId = null;
    state.notice = "Signed out.";
    state.error = "";
  }

  function persistSession(data) {
    state.token = data.token;
    state.user = data.user;

    localStorage.setItem(storageKeys.token, data.token);
    localStorage.setItem(storageKeys.user, JSON.stringify(data.user));
  }

  function handleRequestError(error) {
    if (error?.response?.status === 401) {
      logout();
      state.error = "Your session expired. Sign in again.";
      return;
    }

    state.error = unwrapError(error);
  }

  return {
    state,
    metrics,
    isAuthenticated,
    submitAuth,
    refreshWorkspace,
    uploadSelectedFile,
    downloadSelectedFile,
    deleteSelectedFile,
    createExpiringShareLink,
    revokeExpiringShareLink,
    copyLatestShareLink,
    setAuthMode,
    logout,
  };
}
