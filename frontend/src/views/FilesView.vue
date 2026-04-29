<template>
  <div class="files-page">
    <section class="files-grid">
      <div class="files-column files-column--wide">
        <FileTable
          :files="workspace.state.files"
          :authenticated="workspace.isAuthenticated"
          :busy-download-id="workspace.state.activeDownloadId"
          :busy-delete-id="workspace.state.activeDeleteId"
          :busy-share-file-id="workspace.state.activeShareFileId"
          :busy-revoke-share-id="workspace.state.activeRevokeShareId"
          @download="workspace.downloadSelectedFile"
          @delete="workspace.deleteSelectedFile"
          @refresh="workspace.refreshWorkspace"
          @share="workspace.createExpiringShareLink"
          @revoke-share="workspace.revokeExpiringShareLink"
        />
      </div>

      <div class="files-column">
        <article class="surface-card summary-card">
          <p class="section-kicker">Sharing</p>
          <h3>External access</h3>
          <div class="summary-metrics">
            <div>
              <span>Total files</span>
              <strong>{{ workspace.metrics.totalFiles }}</strong>
            </div>
            <div>
              <span>Active links</span>
              <strong>{{ workspace.metrics.activeShares }}</strong>
            </div>
          </div>
        </article>

        <ShareLinkCard
          :share-link="workspace.state.latestShareLink"
          @copy="workspace.copyLatestShareLink"
        />
      </div>
    </section>
  </div>
</template>

<script>
import FileTable from "../components/workspace/FileTable.vue";
import ShareLinkCard from "../components/workspace/ShareLinkCard.vue";

export default {
  name: "FilesView",
  components: {
    FileTable,
    ShareLinkCard,
  },
  props: {
    workspace: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.files-page,
.files-grid,
.files-column {
  display: grid;
  gap: 24px;
}

.files-grid {
  grid-template-columns: minmax(0, 1.35fr) minmax(300px, 0.65fr);
  align-items: start;
}

.files-column--wide {
  min-width: 0;
}

.summary-card {
  background:
    radial-gradient(circle at top left, rgba(255, 186, 73, 0.14), transparent 38%),
    linear-gradient(180deg, rgba(255, 250, 243, 0.97), rgba(255, 255, 255, 0.94));
}

.section-kicker {
  margin: 0 0 10px;
  font-size: 0.8rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-muted);
}

h3 {
  margin: 0 0 18px;
  font-family: var(--font-display);
  font-size: 1.9rem;
  line-height: 1;
}

.summary-metrics {
  display: grid;
  gap: 14px;
}

.summary-metrics div {
  padding: 16px 18px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.74);
  border: 1px solid rgba(15, 41, 46, 0.08);
}

.summary-metrics span,
.summary-metrics strong {
  display: block;
}

.summary-metrics span {
  color: var(--color-muted);
  font-size: 0.88rem;
}

.summary-metrics strong {
  margin-top: 6px;
  font-size: 1.6rem;
}

@media (max-width: 980px) {
  .files-grid {
    grid-template-columns: 1fr;
  }
}
</style>
