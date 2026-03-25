<template>
  <section class="surface-card">
    <div class="card-header">
      <div>
        <p class="card-kicker">Access</p>
        <h3>{{ authenticated ? "Session active" : "Sign in to operate" }}</h3>
      </div>
      <div class="mode-switch" v-if="!authenticated">
        <button
          :class="['mode-button', { 'mode-button--active': mode === 'login' }]"
          type="button"
          @click="$emit('update:mode', 'login')"
        >
          Login
        </button>
        <button
          :class="['mode-button', { 'mode-button--active': mode === 'register' }]"
          type="button"
          @click="$emit('update:mode', 'register')"
        >
          Register
        </button>
      </div>
    </div>

    <template v-if="authenticated">
      <p class="session-copy">
        Connected as <strong>{{ user.username }}</strong>. The workspace is now
        live for uploads, downloads, and transfer telemetry.
      </p>
      <button class="secondary-button" type="button" @click="$emit('logout')">
        End session
      </button>
    </template>

    <form v-else class="auth-form" @submit.prevent="$emit('submit')">
      <label>
        Username
        <input
          :value="username"
          autocomplete="username"
          placeholder="platform.engineer"
          @input="$emit('update:username', $event.target.value)"
        >
      </label>

      <label>
        Password
        <input
          :value="password"
          type="password"
          autocomplete="current-password"
          placeholder="At least 8 characters"
          @input="$emit('update:password', $event.target.value)"
        >
      </label>

      <button class="primary-button" type="submit" :disabled="busy">
        {{ busy ? "Working..." : mode === "register" ? "Create account" : "Sign in" }}
      </button>
    </form>

    <p v-if="notice" class="status status--success">{{ notice }}</p>
    <p v-if="error" class="status status--error">{{ error }}</p>
  </section>
</template>

<script>
export default {
  name: "AuthCard",
  props: {
    mode: {
      type: String,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
    password: {
      type: String,
      required: true,
    },
    busy: {
      type: Boolean,
      default: false,
    },
    authenticated: {
      type: Boolean,
      default: false,
    },
    user: {
      type: Object,
      default: null,
    },
    notice: {
      type: String,
      default: "",
    },
    error: {
      type: String,
      default: "",
    },
  },
  emits: [
    "logout",
    "submit",
    "update:mode",
    "update:password",
    "update:username",
  ],
};
</script>

<style scoped>
.surface-card {
  display: grid;
  gap: 18px;
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

h3 {
  margin: 0;
  font-size: 1.4rem;
}

.mode-switch {
  display: inline-flex;
  padding: 4px;
  border-radius: 999px;
  background: rgba(18, 43, 57, 0.08);
}

.mode-button {
  border: none;
  border-radius: 999px;
  padding: 10px 14px;
  background: transparent;
  color: var(--color-muted);
}

.mode-button--active {
  background: white;
  color: var(--color-ink);
  box-shadow: 0 6px 16px rgba(18, 43, 57, 0.12);
}

.auth-form {
  display: grid;
  gap: 14px;
}

label {
  display: grid;
  gap: 8px;
  color: var(--color-muted);
  font-weight: 700;
}

input {
  border: 1px solid rgba(18, 43, 57, 0.12);
  border-radius: 16px;
  padding: 14px 16px;
  background: white;
}

.session-copy {
  margin: 0;
  color: var(--color-muted);
}

.status {
  margin: 0;
  padding: 12px 14px;
  border-radius: 16px;
  font-weight: 700;
}

.status--success {
  background: rgba(0, 179, 164, 0.12);
  color: #116f67;
}

.status--error {
  background: rgba(204, 60, 47, 0.12);
  color: #9c3428;
}
</style>
