<template>
  <article class="metric-card">
    <p>{{ title }}</p>
    <strong>{{ value }}</strong>
    <span>{{ hint }}</span>
  </article>
</template>

<script>
export default {
  name: "MetricCard",
  props: {
    title: {
      type: String,
      required: true,
    },
    value: {
      type: String,
      required: true,
    },
    hint: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.metric-card {
  padding: 22px;
  border-radius: 24px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(247, 250, 248, 0.92));
  box-shadow: var(--shadow-soft);
  border: 1px solid rgba(18, 43, 57, 0.08);
}

p,
span,
strong {
  display: block;
}

p {
  margin: 0;
  color: var(--color-muted);
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
}

strong {
  margin: 10px 0 8px;
  font-size: 1.9rem;
  font-family: var(--font-display);
}

span {
  color: var(--color-muted);
}
</style>
