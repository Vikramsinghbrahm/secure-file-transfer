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
      <label class="file-picker">
        <span>{{ selectedFile ? selectedFile.name : "Choose file" }}</span>
        <input type="file" :disabled="!authenticated || busy" @change="onFileChange">
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
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0] || null;
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
  background: rgba(0, 179, 164, 0.12);
  color: #116f67;
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
  justify-content: space-between;
  gap: 12px;
  min-height: 72px;
  padding: 16px 18px;
  border-radius: 18px;
  border: 1px dashed rgba(18, 43, 57, 0.18);
  background: rgba(245, 249, 247, 0.8);
  font-weight: 700;
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
