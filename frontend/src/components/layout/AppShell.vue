<template>
  <div class="app-shell">
    <div class="orb orb--amber"></div>
    <div class="orb orb--teal"></div>

    <header class="app-header surface-card">
      <div class="brand-row">
        <div class="brand-block">
          <p class="eyebrow">Secure file transfer</p>
          <h1>VaultFlow</h1>
          <p class="brand-copy">Controlled exchange for internal and external file delivery.</p>
        </div>

        <div class="header-actions">
          <span class="status-chip">
            {{ isAuthenticated ? "Authenticated" : "Session required" }}
          </span>
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
      </div>

      <nav class="main-nav" aria-label="Primary">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link"
          :class="{ 'nav-link--active': route.path === item.to }"
        >
          <span class="nav-link__label">{{ item.label }}</span>
          <span class="nav-link__copy">{{ item.copy }}</span>
        </RouterLink>
      </nav>
    </header>

    <main class="app-content">
      <section class="page-intro">
        <p class="page-intro__eyebrow">{{ route.meta.kicker }}</p>
        <h2>{{ route.meta.title }}</h2>
        <p class="page-intro__copy">{{ route.meta.description }}</p>
      </section>

      <slot />
    </main>
  </div>
</template>

<script>
import { useRoute } from "vue-router";

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
  setup() {
    const route = useRoute();
    const navItems = [
      { to: "/", label: "Overview", copy: "Status and routing" },
      { to: "/workspace", label: "Workspace", copy: "Access and uploads" },
      { to: "/files", label: "Files", copy: "Catalog and sharing" },
      { to: "/activity", label: "Activity", copy: "Audit and usage" },
    ];

    return {
      navItems,
      route,
    };
  },
};
</script>

<style scoped>
.app-shell {
  position: relative;
  min-height: 100vh;
  padding: 32px 24px 48px;
  overflow: hidden;
}

.orb {
  position: fixed;
  border-radius: 999px;
  filter: blur(24px);
  pointer-events: none;
  opacity: 0.34;
}

.orb--amber {
  top: -120px;
  right: -80px;
  width: 320px;
  height: 320px;
  background: radial-gradient(circle, rgba(255, 186, 73, 0.28), transparent 72%);
}

.orb--teal {
  bottom: -120px;
  left: -80px;
  width: 380px;
  height: 380px;
  background: radial-gradient(circle, rgba(21, 150, 140, 0.18), transparent 74%);
}

.app-header {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 22px;
  max-width: 1240px;
  margin: 0 auto 28px;
  padding: 24px 28px;
}

.brand-row {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-start;
}

.eyebrow,
.page-intro__eyebrow {
  margin: 0 0 10px;
  font-size: 0.78rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--color-muted);
}

h1,
h2 {
  margin: 0;
  font-family: var(--font-display);
  font-weight: 700;
  line-height: 0.94;
  color: var(--color-ink);
}

h1 {
  font-size: clamp(2.4rem, 4vw, 3.8rem);
}

h2 {
  font-size: clamp(1.7rem, 3vw, 2.5rem);
}

.brand-copy,
.page-intro__copy {
  margin: 12px 0 0;
  max-width: 56ch;
  color: var(--color-muted);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.status-chip,
.user-chip {
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(15, 41, 46, 0.06);
  color: var(--color-ink);
  font-weight: 700;
}

.status-chip {
  background: rgba(20, 117, 111, 0.08);
  color: var(--color-accent-strong);
}

.main-nav {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.nav-link {
  display: grid;
  gap: 6px;
  padding: 14px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(15, 41, 46, 0.08);
  color: inherit;
  text-decoration: none;
  transition:
    transform 160ms ease,
    border-color 160ms ease,
    background 160ms ease,
    box-shadow 160ms ease;
}

.nav-link:hover {
  transform: translateY(-1px);
  border-color: rgba(15, 41, 46, 0.14);
  box-shadow: 0 12px 24px rgba(22, 44, 52, 0.06);
}

.nav-link--active {
  background: var(--color-surface-strong);
  border-color: rgba(18, 119, 110, 0.24);
}

.nav-link__label {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
}

.nav-link__copy {
  color: var(--color-muted);
  font-size: 0.9rem;
}

.app-content {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 20px;
  max-width: 1240px;
  margin: 0 auto;
}

.page-intro {
  padding: 4px 4px 0;
}

@media (max-width: 980px) {
  .brand-row {
    flex-direction: column;
  }

  .header-actions {
    justify-content: flex-start;
  }

  .main-nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .app-shell {
    padding-inline: 16px;
  }

  .app-header {
    padding: 20px;
  }

  .main-nav {
    grid-template-columns: 1fr;
  }
}
</style>
