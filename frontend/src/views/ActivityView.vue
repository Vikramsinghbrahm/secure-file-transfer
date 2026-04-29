<template>
  <div class="activity-page">
    <section class="activity-grid">
      <div class="metrics-column">
        <MetricCard
          title="Downloads"
          :value="String(workspace.metrics.downloadCount)"
          hint="Completed retrievals"
        />
        <MetricCard
          title="Active links"
          :value="String(workspace.metrics.activeShares)"
          hint="Current external shares"
        />
        <article class="surface-card summary-card">
          <p class="section-kicker">Audit</p>
          <h3>Recent activity</h3>
          <p>Authentication, uploads, downloads, and link usage appear here.</p>
        </article>
      </div>

      <ActivityFeed
        :activity="workspace.state.dashboard.activity"
        :authenticated="workspace.isAuthenticated"
      />
    </section>
  </div>
</template>

<script>
import ActivityFeed from "../components/workspace/ActivityFeed.vue";
import MetricCard from "../components/workspace/MetricCard.vue";

export default {
  name: "ActivityView",
  components: {
    ActivityFeed,
    MetricCard,
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
.activity-page,
.activity-grid,
.metrics-column {
  display: grid;
  gap: 24px;
}

.activity-grid {
  grid-template-columns: minmax(280px, 360px) minmax(0, 1fr);
  align-items: start;
}

.summary-card {
  background:
    radial-gradient(circle at top right, rgba(123, 164, 194, 0.14), transparent 34%),
    linear-gradient(180deg, rgba(239, 246, 250, 0.97), rgba(255, 255, 255, 0.94));
}

.section-kicker {
  margin: 0 0 10px;
  font-size: 0.8rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-muted);
}

h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.9rem;
  line-height: 1;
}

.summary-card p:last-child {
  margin-bottom: 0;
  color: var(--color-muted);
}

@media (max-width: 980px) {
  .activity-grid {
    grid-template-columns: 1fr;
  }
}
</style>
