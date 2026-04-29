<template>
  <div class="overview-page">
    <TransferOverviewPanel
      :is-authenticated="workspace.isAuthenticated"
      :user="workspace.state.user"
      :metrics="workspace.metrics"
    />

    <section class="overview-actions">
      <RouterLink to="/workspace" class="action-card">
        <p class="section-kicker">Workspace</p>
        <h3>Access and upload</h3>
        <p>Manage authentication and add new files.</p>
      </RouterLink>

      <RouterLink to="/files" class="action-card">
        <p class="section-kicker">Files</p>
        <h3>Storage and links</h3>
        <p>Review stored artifacts and external sharing.</p>
      </RouterLink>

      <RouterLink to="/activity" class="action-card">
        <p class="section-kicker">Activity</p>
        <h3>Audit and usage</h3>
        <p>Track downloads, links, and recent events.</p>
      </RouterLink>
    </section>

    <section class="metric-grid">
      <MetricCard
        title="Stored files"
        :value="String(workspace.metrics.totalFiles)"
        hint="Current artifact count"
      />
      <MetricCard
        title="Storage used"
        :value="formatBytes(workspace.metrics.storageBytes)"
        hint="Allocated workspace storage"
      />
      <MetricCard
        title="Active links"
        :value="String(workspace.metrics.activeShares)"
        hint="Open external share links"
      />
    </section>
  </div>
</template>

<script>
import TransferOverviewPanel from "../components/home/TransferOverviewPanel.vue";
import MetricCard from "../components/workspace/MetricCard.vue";
import { formatBytes } from "../utils/formatters";

export default {
  name: "OverviewView",
  components: {
    MetricCard,
    TransferOverviewPanel,
  },
  props: {
    workspace: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatBytes,
  },
};
</script>

<style scoped>
.overview-page,
.overview-actions,
.metric-grid {
  display: grid;
  gap: 24px;
}

.overview-actions,
.metric-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.action-card {
  display: grid;
  gap: 10px;
  padding: 26px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(15, 41, 46, 0.08);
  box-shadow: var(--shadow-soft);
  color: inherit;
  text-decoration: none;
  transition:
    transform 160ms ease,
    border-color 160ms ease,
    box-shadow 160ms ease;
}

.action-card:hover {
  transform: translateY(-2px);
  border-color: rgba(20, 117, 111, 0.18);
  box-shadow: 0 18px 30px rgba(22, 44, 52, 0.08);
}

.section-kicker {
  margin: 0;
  font-size: 0.78rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-muted);
}

h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.6rem;
  line-height: 1;
}

.action-card p:last-child {
  margin: 0;
  color: var(--color-muted);
}

@media (max-width: 980px) {
  .overview-actions,
  .metric-grid {
    grid-template-columns: 1fr;
  }
}
</style>
