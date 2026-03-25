<template>
  <section class="overview-panel">
    <div class="overview-panel__content">
      <p class="overview-panel__eyebrow">Transfer control plane</p>
      <h2 class="overview-panel__title">
        Secure sharing, streamed transfers, and operational guardrails.
      </h2>
      <p class="overview-panel__description">
        VaultFlow combines JWT-authenticated access, expiring public share
        links, streamed upload and download paths, rate-limited ingress, and a
        live audit feed into a transfer workflow designed for controlled file exchange.
      </p>

      <div class="overview-panel__capabilities">
        <span>Expiring credential-free share links</span>
        <span>Streamed file transfer paths</span>
        <span>SHA-256 integrity metadata</span>
        <span>Audit events and rate-limited entrypoints</span>
      </div>
    </div>

    <div class="overview-panel__stats">
      <div class="overview-panel__stat-card">
        <span class="overview-panel__stat-label">Authenticated operator</span>
        <strong>{{ isAuthenticated ? user.username : "Not signed in" }}</strong>
      </div>
      <div class="overview-panel__stat-card">
        <span class="overview-panel__stat-label">Managed artifacts</span>
        <strong>{{ metrics.totalFiles }}</strong>
      </div>
      <div class="overview-panel__stat-card">
        <span class="overview-panel__stat-label">Completed downloads</span>
        <strong>{{ metrics.downloadCount }}</strong>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "TransferOverviewPanel",
  props: {
    isAuthenticated: {
      type: Boolean,
      default: false,
    },
    user: {
      type: Object,
      default: null,
    },
    metrics: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.overview-panel {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
  gap: 24px;
  padding: 32px;
  border-radius: 32px;
  background:
    radial-gradient(circle at top left, rgba(0, 179, 164, 0.25), transparent 34%),
    linear-gradient(135deg, rgba(247, 249, 244, 0.95), rgba(231, 242, 255, 0.92));
  box-shadow: var(--shadow-soft);
  border: 1px solid rgba(18, 43, 57, 0.08);
}

.overview-panel__eyebrow {
  margin: 0 0 14px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-size: 0.85rem;
  color: var(--color-accent);
}

.overview-panel__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 3.6rem);
  line-height: 1;
  max-width: 11ch;
}

.overview-panel__description {
  margin: 20px 0 0;
  max-width: 60ch;
  font-size: 1.05rem;
  color: var(--color-muted);
}

.overview-panel__capabilities {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.overview-panel__capabilities span {
  padding: 12px 16px;
  border-radius: 999px;
  background: rgba(18, 43, 57, 0.06);
  font-weight: 700;
}

.overview-panel__stats {
  display: grid;
  gap: 16px;
  align-content: center;
}

.overview-panel__stat-card {
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(18, 43, 57, 0.08);
}

.overview-panel__stat-card strong {
  display: block;
  margin-top: 8px;
  font-size: 1.75rem;
  color: var(--color-ink);
}

.overview-panel__stat-label {
  color: var(--color-muted);
  font-size: 0.9rem;
}

@media (max-width: 920px) {
  .overview-panel {
    grid-template-columns: 1fr;
  }

  .overview-panel__title {
    max-width: none;
  }
}
</style>
