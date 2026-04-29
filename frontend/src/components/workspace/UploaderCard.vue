<template>
  <section class="surface-card uploader-card">
    <div class="card-header">
      <div>
        <p class="card-kicker">Transfer ingest</p>
        <h3>Upload a new secure artifact</h3>
      </div>
      <span class="card-badge">{{ authenticated ? "Ready" : "Locked" }}</span>
    </div>

    <p class="support-copy">
      Files are stored inside user-scoped directories and enriched with SHA-256
      checksums for traceable retrieval.
    </p>

    <form class="upload-form" @submit.prevent="submitFile">
      <label
        class="file-picker"
        :class="{ 'file-picker--drag-over': dragging, 'file-picker--has-file': !!selectedFile }"
        @dragenter.prevent="onDragEnter"
        @dragover.prevent
        @dragleave="onDragLeave"
        @drop.prevent="onDrop"
      >
        <span class="file-picker__icon" aria-hidden="true">
          {{ selectedFile ? "FILE" : "UPLOAD" }}
        </span>
        <span class="file-picker__label">
          {{ selectedFile ? selectedFile.name : dragging ? "Drop to attach" : "Choose or drop a file" }}
        </span>
        <input
          type="file"
          :disabled="!authenticated || busy"
          @change="onFileChange"
          aria-label="Select file to upload"
        >
      </label>

      <button
        class="primary-button"
        type="submit"
        :disabled="!authenticated || busy || !selectedFile"
      >
        {{ busy ? "Uploading..." : "Upload artifact" }}
      </button>
    </form>

    <div class="recent-list">
      <p class="recent-list__title">Recent arrivals</p>
      <ul v-if="recentFiles.length">
        <li v-for="file in recentFiles" :key="file.id">{{ file.name }}</li>
      </ul>
      <p v-else class="support-copy">No uploads yet. Ship the first artifact.</p>
    </div>
  </section>
</template>

<script>
export default {
  name: "UploaderCard",
  props: {
    authenticated: {
      type: Boolean,
      default: false,
    },
    busy: {
      type: Boolean,
      default: false,
    },
    recentFiles: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["upload"],
  data() {
    return {
      selectedFile: null,
      dragging: false,
      _dragCounter: 0,
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0] || null;
    },
    onDragEnter() {
      if (!this.authenticated || this.busy) return;
      this._dragCounter++;
      this.dragging = true;
    },
    onDragLeave() {
      this._dragCounter--;
      if (this._dragCounter <= 0) {
        this._dragCounter = 0;
        this.dragging = false;
      }
    },
    onDrop(event) {
      this._dragCounter = 0;
      this.dragging = false;
      if (!this.authenticated || this.busy) return;
      const file = event.dataTransfer?.files?.[0];
      if (file) {
        this.selectedFile = file;
      }
    },
    submitFile() {
      const fileInput = this.$el.querySelector("input[type='file']");
      this.$emit("upload", this.selectedFile);
      this.selectedFile = null;
      if (fileInput) {
        fileInput.value = "";
      }
    },
  },
};
</script>

<style scoped>
.uploader-card {
  display: grid;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.card-kicker {
  margin: 0 0 6px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.75rem;
  color: var(--color-muted);
}

h3,
.support-copy,
.recent-list__title,
ul {
  margin: 0;
}

.card-badge {
  align-self: flex-start;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(20, 117, 111, 0.12);
  color: var(--color-accent-strong);
  font-weight: 800;
}

.support-copy {
  color: var(--color-muted);
}

.upload-form {
  display: grid;
  gap: 14px;
}

.file-picker {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 72px;
  padding: 16px 18px;
  border-radius: 20px;
  border: 1.5px dashed rgba(24, 50, 60, 0.18);
  background: rgba(250, 248, 243, 0.92);
  font-weight: 700;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}

.file-picker--drag-over {
  border-color: var(--color-accent);
  background: rgba(20, 117, 111, 0.07);
}

.file-picker--has-file {
  border-style: solid;
  border-color: rgba(20, 117, 111, 0.45);
}

.file-picker__icon {
  flex-shrink: 0;
  padding: 8px 10px;
  border-radius: 12px;
  background: rgba(24, 50, 60, 0.08);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
}

.file-picker__label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-picker input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.recent-list {
  display: grid;
  gap: 10px;
  padding-top: 6px;
}

.recent-list__title {
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--color-muted);
}

ul {
  padding-left: 18px;
  color: var(--color-ink);
}
</style>
