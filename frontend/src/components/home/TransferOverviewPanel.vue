<template>
  <section class="overview-panel">
    <div class="overview-panel__content">
      <p class="overview-panel__eyebrow">Workspace status</p>
      <h2 class="overview-panel__title">Secure transfer workspace</h2>
      <p class="overview-panel__description">
        Upload, distribute, and review transfer activity from a single authenticated workspace.
      </p>

      <div class="overview-panel__capabilities">
        <span>Authenticated access</span>
        <span>Expiring links</span>
        <span>Integrity metadata</span>
        <span>Audit records</span>
      </div>
    </div>

    <div class="overview-panel__stats">
      <div class="overview-panel__stat-card">
        <span class="overview-panel__stat-label">Session</span>
        <strong>{{ isAuthenticated ? user.username : "Not signed in" }}</strong>
      </div>
      <div class="overview-panel__stat-card">
        <span class="overview-panel__stat-label">Files</span>
        <strong>{{ metrics.totalFiles }}</strong>
      </div>
      <div class="overview-panel__stat-card">
        <span class="overview-panel__stat-label">Active links</span>
        <strong>{{ metrics.activeShares }}</strong>
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
    radial-gradient(circle at top left, rgba(20, 117, 111, 0.16), transparent 34%),
    linear-gradient(135deg, rgba(251, 249, 245, 0.97), rgba(240, 245, 245, 0.94));
  box-shadow: var(--shadow-soft);
  border: 1px solid rgba(18, 43, 57, 0.08);
}

.overview-panel__eyebrow {
  margin: 0 0 14px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-size: 0.82rem;
  color: var(--color-accent);
}

.overview-panel__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 3.3rem);
  line-height: 0.96;
}

.overview-panel__description {
  margin: 18px 0 0;
  max-width: 52ch;
  color: var(--color-muted);
}

.overview-panel__capabilities {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
}

.overview-panel__capabilities span {
  padding: 11px 14px;
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
  padding: 20px 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.84);
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
}
</style>
