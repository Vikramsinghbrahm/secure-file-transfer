<template>
  <section v-if="shareLink" class="surface-card share-link-card">
    <div class="card-header">
      <div>
        <p class="card-kicker">External access</p>
        <h3>Latest expiring share link</h3>
      </div>
      <button class="primary-button" type="button" @click="$emit('copy')">
        Copy link
      </button>
    </div>

    <p class="support-copy">
      Created for <strong>{{ shareLink.fileName }}</strong>. Recipients can
      download without credentials until the link expires or its single-download
      budget is consumed.
    </p>

    <div class="share-url-row">
      <input
        class="share-url"
        :value="shareLink.shareUrl"
        readonly
        @focus="$event.target.select()"
        @click="$event.target.select()"
      >
      <button class="secondary-button share-copy-button" type="button" @click="$emit('copy')">
        Copy URL
      </button>
    </div>

    <div class="share-meta">
      <span>Expires {{ formatDate(shareLink.expiresAt) }}</span>
      <span>{{ shareLink.maxDownloads }} allowed download</span>
      <span>{{ shareLink.tokenPreview }}</span>
    </div>
  </section>
</template>

<script>
import { formatDate } from "../../utils/formatters";

export default {
  name: "ShareLinkCard",
  props: {
    shareLink: {
      type: Object,
      default: null,
    },
  },
  emits: ["copy"],
  methods: {
    formatDate,
  },
};
</script>

<style scoped>
.share-link-card {
  display: grid;
  gap: 16px;
}

.card-header {
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

h3,
.support-copy {
  margin: 0;
}

.support-copy {
  color: var(--color-muted);
}

.share-url {
  width: 100%;
  border: 1px solid rgba(18, 43, 57, 0.12);
  border-radius: 16px;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.9);
  color: var(--color-ink);
  font-family: var(--font-mono);
}

.share-url-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: center;
}

.share-copy-button {
  white-space: nowrap;
}

.share-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.share-meta span {
  padding: 10px 12px;
  border-radius: 999px;
  background: rgba(18, 43, 57, 0.06);
  color: var(--color-muted);
  font-size: 0.9rem;
}

@media (max-width: 720px) {
  .card-header,
  .share-url-row {
    grid-template-columns: 1fr;
  }

  .card-header {
    display: grid;
  }
}
</style>
