<template>
  <div class="app-shell">
    <header class="app-header">
      <div>
        <p class="eyebrow">Secure file transfer system</p>
        <h1>VaultFlow</h1>
      </div>

      <div class="header-actions">
        <span v-if="isAuthenticated" class="user-chip">
          {{ user.username }}
        </span>
        <button
          v-if="isAuthenticated"
          class="ghost-button"
          type="button"
          @click="$emit('logout')"
        >
          Sign out
        </button>
      </div>
    </header>

    <main class="app-content">
      <slot />
    </main>
  </div>
</template>

<script>
export default {
  name: "AppShell",
  props: {
    isAuthenticated: {
      type: Boolean,
      default: false,
    },
    user: {
      type: Object,
      default: null,
    },
  },
  emits: ["logout"],
};
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  padding: 32px 24px 48px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: center;
  max-width: 1240px;
  margin: 0 auto 32px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.85rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-muted);
}

h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 3.5rem);
  line-height: 0.95;
  color: var(--color-ink);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-chip {
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(18, 43, 57, 0.08);
  color: var(--color-ink);
  font-weight: 700;
}

.ghost-button {
  border: 1px solid rgba(18, 43, 57, 0.16);
  background: rgba(255, 255, 255, 0.7);
  color: var(--color-ink);
}

.app-content {
  max-width: 1240px;
  margin: 0 auto;
}

@media (max-width: 700px) {
  .app-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
