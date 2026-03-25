<template>
  <section class="surface-card activity-card">
    <div class="card-header">
      <div>
        <p class="card-kicker">Audit trail</p>
        <h3>Recent activity</h3>
      </div>
    </div>

    <div v-if="!authenticated" class="empty-state">
      Activity is populated after authentication events and transfer actions.
    </div>

    <ul v-else-if="activity.length" class="activity-list">
      <li v-for="item in activity" :key="item.id">
        <span class="activity-action">{{ item.action }}</span>
        <strong>{{ item.description }}</strong>
        <span class="activity-time">{{ formatDate(item.createdAt) }}</span>
      </li>
    </ul>

    <div v-else class="empty-state">No activity yet.</div>
  </section>
</template>

<script>
import { formatDate } from "../../utils/formatters";

export default {
  name: "ActivityFeed",
  props: {
    activity: {
      type: Array,
      default: () => [],
    },
    authenticated: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    formatDate,
  },
};
</script>

<style scoped>
.activity-card {
  display: grid;
  gap: 18px;
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

.activity-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 12px;
}

.activity-list li {
  display: grid;
  gap: 6px;
  padding: 18px;
  border-radius: 20px;
  background: rgba(18, 43, 57, 0.04);
}

.activity-action {
  color: var(--color-accent);
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.activity-time,
.empty-state {
  color: var(--color-muted);
}

.empty-state {
  padding: 24px;
  border-radius: 20px;
  background: rgba(18, 43, 57, 0.04);
}
</style>
