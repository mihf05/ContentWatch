<script setup>
const CHART_HEIGHT_PX = 128

const props = defineProps({
  bars: { type: Array, required: true },
})

const pct = (v) => Math.round((v ?? 0) * 100)

const maxPct = computed(() => {
  const values = props.bars.map((b) => pct(b.value))
  return Math.max(...values, 1)
})

function barHeightPx(bar) {
  const scaled = (pct(bar.value) / maxPct.value) * CHART_HEIGHT_PX
  return Math.max(Math.round(scaled), 10)
}

function barStyle(bar) {
  return {
    height: `${barHeightPx(bar)}px`,
    background: `linear-gradient(to top, ${bar.color}66, ${bar.color})`,
  }
}

const chartSummary = computed(() =>
  props.bars.map((b) => `${b.label} ${pct(b.value)}%`).join(', ')
)
</script>

<template>
  <div class="grid grid-cols-3 gap-3 sm:gap-5 mt-2" role="img" :aria-label="`Length preference: ${chartSummary}`">
    <div v-for="bar in bars" :key="bar.label" class="flex flex-col items-center min-w-0">
      <span class="text-xs font-bold tabular-nums mb-2 shrink-0" :style="{ color: bar.color }">
        {{ pct(bar.value) }}%
      </span>

      <div
        class="relative w-full max-w-14 sm:max-w-16 mx-auto flex items-end justify-center rounded-lg bg-white/3 border border-white/4"
        :style="{ height: `${CHART_HEIGHT_PX}px` }">
        <div class="w-10 sm:w-12 rounded-t-xl transition-[height] duration-1000 ease-out" :style="barStyle(bar)" />
      </div>

      <span class="text-[11px] text-gray-500 mt-2 text-center leading-tight">
        {{ bar.label }}
      </span>
    </div>
  </div>
</template>
