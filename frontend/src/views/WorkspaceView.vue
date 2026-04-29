<template>
  <div class="workspace-page">
    <section class="workspace-grid">
      <div class="workspace-column">
        <AuthCard
          :mode="workspace.state.authMode"
          :username="workspace.state.username"
          :password="workspace.state.password"
          :busy="workspace.state.isAuthenticating"
          :authenticated="workspace.isAuthenticated"
          :user="workspace.state.user"
          :notice="workspace.state.notice"
          :error="workspace.state.error"
          @submit="workspace.submitAuth"
          @logout="workspace.logout"
          @update:mode="workspace.setAuthMode"
          @update:username="workspace.state.username = $event"
          @update:password="workspace.state.password = $event"
        />

        <div class="metrics-grid">
          <MetricCard
            title="Stored files"
            :value="String(workspace.metrics.totalFiles)"
            hint="Workspace artifact count"
          />
          <MetricCard
            title="Storage used"
            :value="formatBytes(workspace.metrics.storageBytes)"
            hint="Current storage footprint"
          />
        </div>
      </div>

      <div class="workspace-column workspace-column--wide">
        <article class="surface-card summary-card">
          <p class="section-kicker">Session</p>
          <h3>{{ workspace.isAuthenticated ? "Workspace ready" : "Sign in required" }}</h3>
          <p>
            {{ workspace.isAuthenticated
              ? "Upload and file actions are available."
              : "Authentication is required before upload, download, and sharing actions are enabled." }}
          </p>
        </article>

        <UploaderCard
          :authenticated="workspace.isAuthenticated"
          :busy="workspace.state.isUploading"
          :recent-files="workspace.state.dashboard.recentFiles"
          @upload="workspace.uploadSelectedFile"
        />
      </div>
    </section>
  </div>
</template>

<script>
import AuthCard from "../components/workspace/AuthCard.vue";
import MetricCard from "../components/workspace/MetricCard.vue";
import UploaderCard from "../components/workspace/UploaderCard.vue";
import { formatBytes } from "../utils/formatters";

export default {
  name: "WorkspaceView",
  components: {
    AuthCard,
    MetricCard,
    UploaderCard,
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
.workspace-page {
  display: grid;
  gap: 28px;
}

.workspace-grid {
  display: grid;
  grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
  gap: 24px;
  align-items: start;
}

.workspace-column {
  display: grid;
  gap: 24px;
}

.workspace-column--wide {
  min-width: 0;
}

.metrics-grid {
  display: grid;
  gap: 16px;
}

.summary-card {
  background:
    radial-gradient(circle at top right, rgba(21, 150, 140, 0.12), transparent 30%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 247, 0.92));
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
  .workspace-grid {
    grid-template-columns: 1fr;
  }
}
</style>
