<template>
  <AppShell
    :is-authenticated="workspace.isAuthenticated"
    :user="workspace.state.user"
    @logout="workspace.logout"
  >
    <router-view v-slot="{ Component }">
      <component :is="Component" :workspace="workspace" />
    </router-view>
  </AppShell>
</template>

<script>
import { reactive } from "vue";

import AppShell from "./components/layout/AppShell.vue";
import { useTransferWorkspace } from "./composables/useTransferWorkspace";

export default {
  name: "App",
  components: {
    AppShell,
  },
  setup() {
    const transferWorkspace = useTransferWorkspace();
    const workspace = reactive({
      state: transferWorkspace.state,
      get metrics() {
        return transferWorkspace.metrics.value;
      },
      get isAuthenticated() {
        return transferWorkspace.isAuthenticated.value;
      },
      submitAuth: transferWorkspace.submitAuth,
      refreshWorkspace: transferWorkspace.refreshWorkspace,
      uploadSelectedFile: transferWorkspace.uploadSelectedFile,
      downloadSelectedFile: transferWorkspace.downloadSelectedFile,
      deleteSelectedFile: transferWorkspace.deleteSelectedFile,
      createExpiringShareLink: transferWorkspace.createExpiringShareLink,
      revokeExpiringShareLink: transferWorkspace.revokeExpiringShareLink,
      copyLatestShareLink: transferWorkspace.copyLatestShareLink,
      setAuthMode: transferWorkspace.setAuthMode,
      logout: transferWorkspace.logout,
    });

    return {
      workspace,
    };
  },
};
</script>
