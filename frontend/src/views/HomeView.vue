<template>
  <AppShell
    :is-authenticated="isAuthenticated"
    :user="state.user"
    @logout="logout"
  >
    <div class="workspace-page">
      <TransferOverviewPanel
        :is-authenticated="isAuthenticated"
        :user="state.user"
        :metrics="metrics"
      />

      <section class="workspace-grid">
        <div class="workspace-column">
          <AuthCard
            :mode="state.authMode"
            :username="state.username"
            :password="state.password"
            :busy="state.isAuthenticating"
            :authenticated="isAuthenticated"
            :user="state.user"
            :notice="state.notice"
            :error="state.error"
            @submit="submitAuth"
            @logout="logout"
            @update:mode="setAuthMode"
            @update:username="state.username = $event"
            @update:password="state.password = $event"
          />

          <div class="metrics-grid">
            <MetricCard
              title="Files in scope"
              :value="String(metrics.totalFiles)"
              hint="Cataloged artifacts owned by the signed-in user."
            />
            <MetricCard
              title="Storage footprint"
              :value="formatBytes(metrics.storageBytes)"
              hint="Persisted bytes under isolated storage."
            />
            <MetricCard
              title="Download volume"
              :value="String(metrics.downloadCount)"
              hint="Successful retrieval operations recorded."
            />
            <MetricCard
              title="Active share links"
              :value="String(metrics.activeShares)"
              hint="Credential-free external download windows currently open."
            />
          </div>

          <UploaderCard
            :authenticated="isAuthenticated"
            :busy="state.isUploading"
            :recent-files="state.dashboard.recentFiles"
            @upload="uploadSelectedFile"
          />

          <ShareLinkCard
            :share-link="state.latestShareLink"
            @copy="copyLatestShareLink"
          />
        </div>

        <div class="workspace-column workspace-column--wide">
          <FileTable
            :files="state.files"
            :authenticated="isAuthenticated"
            :busy-download-id="state.activeDownloadId"
            :busy-delete-id="state.activeDeleteId"
            :busy-share-file-id="state.activeShareFileId"
            :busy-revoke-share-id="state.activeRevokeShareId"
            @download="downloadSelectedFile"
            @delete="deleteSelectedFile"
            @refresh="refreshWorkspace"
            @share="createExpiringShareLink"
            @revoke-share="revokeExpiringShareLink"
          />

          <ActivityFeed
            :activity="state.dashboard.activity"
            :authenticated="isAuthenticated"
          />
        </div>
      </section>
    </div>
  </AppShell>
</template>

<script>
import AppShell from "../components/layout/AppShell.vue";
import TransferOverviewPanel from "../components/home/TransferOverviewPanel.vue";
import ActivityFeed from "../components/workspace/ActivityFeed.vue";
import AuthCard from "../components/workspace/AuthCard.vue";
import FileTable from "../components/workspace/FileTable.vue";
import MetricCard from "../components/workspace/MetricCard.vue";
import ShareLinkCard from "../components/workspace/ShareLinkCard.vue";
import UploaderCard from "../components/workspace/UploaderCard.vue";
import { useTransferWorkspace } from "../composables/useTransferWorkspace";
import { formatBytes } from "../utils/formatters";

export default {
  name: "HomeView",
  components: {
    ActivityFeed,
    AppShell,
    AuthCard,
    FileTable,
    TransferOverviewPanel,
    MetricCard,
    ShareLinkCard,
    UploaderCard,
  },
  setup() {
    const workspace = useTransferWorkspace();

    return {
      ...workspace,
      formatBytes,
    };
  },
};
</script>

<style scoped>
.workspace-page {
  display: grid;
  gap: 28px;
}

.workspace-grid {
  display: grid;
  grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
  gap: 24px;
  align-items: start;
}

.workspace-column {
  display: grid;
  gap: 24px;
}

.workspace-column--wide {
  min-width: 0;
}

.metrics-grid {
  display: grid;
  gap: 16px;
}

@media (max-width: 980px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }
}
</style>
