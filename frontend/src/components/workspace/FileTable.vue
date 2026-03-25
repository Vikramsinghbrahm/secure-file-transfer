<template>
  <section class="surface-card files-card">
    <div class="table-header">
      <div>
        <p class="card-kicker">Managed artifacts</p>
        <h3>Workspace files</h3>
      </div>
      <button class="ghost-button" type="button" @click="$emit('refresh')">
        Refresh
      </button>
    </div>

    <div v-if="!authenticated" class="empty-state">
      Sign in to view the secure artifact catalog.
    </div>

    <div v-else-if="!files.length" class="empty-state">
      No files are stored yet. Upload an artifact to generate metadata and audit
      events.
    </div>

    <div v-else class="table-wrapper">
      <table class="files-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Size</th>
            <th>Checksum</th>
            <th>Uploaded</th>
            <th>Downloads</th>
            <th>Share links</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="file in files" :key="file.id">
            <td class="file-cell">
              <strong class="file-name">{{ file.name }}</strong>
              <span class="file-type">{{ file.contentType }}</span>
            </td>
            <td class="cell-center">{{ formatBytes(file.sizeBytes) }}</td>
            <td class="checksum cell-center">{{ compactChecksum(file.checksumSha256) }}</td>
            <td class="cell-center">{{ formatDate(file.createdAt) }}</td>
            <td class="cell-center">{{ file.downloadCount }}</td>
            <td class="share-cell">
              <div v-if="file.activeShareLinks.length" class="share-list">
                <div
                  v-for="share in file.activeShareLinks"
                  :key="share.id"
                  class="share-pill"
                >
                  <strong>{{ share.tokenPreview }}</strong>
                  <span>Expires {{ formatDate(share.expiresAt) }}</span>
                  <span>{{ share.downloadCount }}/{{ share.maxDownloads }} used</span>
                  <button
                    class="ghost-button ghost-button--small"
                    type="button"
                    :disabled="busyRevokeShareId === share.id"
                    @click="$emit('revoke-share', share)"
                  >
                    {{ busyRevokeShareId === share.id ? "Revoking..." : "Revoke" }}
                  </button>
                </div>
              </div>
              <span v-else class="muted-inline">None</span>
            </td>
            <td class="action-cell">
              <div class="action-row">
              <button
                class="secondary-button"
                type="button"
                :disabled="busyShareFileId === file.id"
                @click="$emit('share', file)"
              >
                {{ busyShareFileId === file.id ? "Creating..." : "Create link" }}
              </button>
              <button
                class="secondary-button"
                type="button"
                :disabled="busyDownloadId === file.id"
                @click="$emit('download', file)"
              >
                {{ busyDownloadId === file.id ? "Downloading..." : "Download" }}
              </button>
              <button
                class="ghost-button"
                type="button"
                :disabled="busyDeleteId === file.id"
                @click="$emit('delete', file)"
              >
                {{ busyDeleteId === file.id ? "Deleting..." : "Delete" }}
              </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
import { compactChecksum, formatBytes, formatDate } from "../../utils/formatters";

export default {
  name: "FileTable",
  props: {
    files: {
      type: Array,
      default: () => [],
    },
    authenticated: {
      type: Boolean,
      default: false,
    },
    busyDownloadId: {
      type: String,
      default: null,
    },
    busyDeleteId: {
      type: String,
      default: null,
    },
    busyShareFileId: {
      type: String,
      default: null,
    },
    busyRevokeShareId: {
      type: String,
      default: null,
    },
  },
  emits: ["delete", "download", "refresh", "revoke-share", "share"],
  methods: {
    compactChecksum,
    formatBytes,
    formatDate,
  },
};
</script>

<style scoped>
.files-card {
  display: grid;
  gap: 18px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.card-kicker {
  margin: 0 0 6px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.75rem;
  color: var(--color-muted);
}

h3 {
  margin: 0;
}

.table-wrapper {
  overflow-x: auto;
  margin-inline: -4px;
  padding-inline: 4px;
}

.files-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  min-width: 980px;
}

th {
  text-align: center;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--color-muted);
  padding: 0 12px 14px;
}

td {
  padding: 18px 12px;
  border-top: 1px solid rgba(18, 43, 57, 0.08);
  vertical-align: middle;
}

.file-cell {
  min-width: 0;
}

.file-name,
.file-type {
  display: block;
  overflow-wrap: anywhere;
}

.file-type {
  margin-top: 6px;
  color: var(--color-muted);
  font-size: 0.9rem;
}

.cell-center {
  text-align: center;
}

.checksum {
  font-family: var(--font-mono);
  color: var(--color-muted);
  overflow-wrap: anywhere;
}

.share-cell,
.action-cell {
  min-width: 0;
}

.action-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.share-list {
  display: grid;
  gap: 10px;
}

.share-pill {
  display: grid;
  gap: 6px;
  padding: 12px;
  border-radius: 16px;
  background: rgba(18, 43, 57, 0.04);
  min-width: 0;
}

.share-pill strong {
  font-family: var(--font-mono);
  overflow-wrap: anywhere;
}

.ghost-button--small {
  min-height: 36px;
  width: fit-content;
  padding: 8px 12px;
}

.muted-inline {
  color: var(--color-muted);
  display: inline-block;
  width: 100%;
  text-align: center;
}

.empty-state {
  padding: 32px;
  border-radius: 24px;
  background: rgba(18, 43, 57, 0.04);
  color: var(--color-muted);
}

@media (max-width: 1100px) {
  .files-table {
    min-width: 900px;
  }
}
</style>
