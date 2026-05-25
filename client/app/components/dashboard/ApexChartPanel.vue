<script setup>
const props = defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  icon: { type: String, default: 'bar_chart' },
  accent: { type: String, default: 'brand' },
  loading: { type: Boolean, default: false },
  chart: { type: Object, default: null },
  type: { type: String, default: 'line' },
  height: { type: [Number, String], default: 300 },
  panelClass: { type: String, default: '' },
  featured: { type: Boolean, default: false },
})

const hasChart = computed(() => Boolean(props.chart?.series?.length && props.chart?.options))

const accentGlow = computed(() => {
  const map = {
    brand: 'rgba(77, 220, 198, 0.12)',
    purple: 'rgba(124, 111, 255, 0.12)',
    amber: 'rgba(245, 158, 11, 0.1)',
    orange: 'rgba(249, 115, 22, 0.1)',
  }
  return map[props.accent] ?? map.brand
})
</script>

<template>
  <section class="chart-panel" :class="[
    panelClass,
    featured ? 'chart-panel--featured' : '',
    `chart-panel--${accent}`,
  ]">
    <div class="chart-panel__glow" :style="{ background: accentGlow }" aria-hidden="true" />
    <div class="chart-panel__ring" aria-hidden="true" />

    <header class="chart-panel__header">
      <div class="chart-panel__icon" :class="`chart-panel__icon--${accent}`">
        <span class="material-symbols-outlined text-xl">{{ icon }}</span>
      </div>
      <div class="min-w-0 flex-1">
        <h3 class="text-headline-md text-white">{{ title }}</h3>
        <p v-if="description" class="text-body-sm text-gray-500 mt-0.5 line-clamp-2">
          {{ description }}
        </p>
      </div>
    </header>

    <div class="chart-panel__body">
      <div v-if="loading" class="chart-panel__skeleton" :style="{ height: `${height}px` }" />

      <div v-else-if="!hasChart" class="chart-panel__empty" :style="{ height: `${height}px` }">
        <span class="material-symbols-outlined text-3xl text-gray-600">query_stats</span>
        <p class="text-body-sm text-gray-500">No data available yet</p>
      </div>

      <ClientOnly v-else>
        <div class="chart-panel__plot chart-apex-root">
          <apexchart
            width="100%"
            :type="type"
            :height="height"
            :options="chart.options"
            :series="chart.series"
          />
        </div>
        <template #fallback>
          <div class="chart-panel__skeleton" :style="{ height: `${height}px` }" />
        </template>
      </ClientOnly>
    </div>
  </section>
</template>
