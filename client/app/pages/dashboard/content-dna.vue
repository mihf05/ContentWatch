<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

useHead({ title: 'Content DNA' })

const { apiFetch } = useApiFetch()
const { showError } = usePopup()

const dnaData = ref(null)
const isLoading = ref(true)
const fetchError = ref(null)

async function loadDNA() {
  isLoading.value = true
  fetchError.value = null
  try {
    const data = await apiFetch('/user/contentdna')
    dnaData.value = data
  } catch (err) {
    showError(err, 'Could not retrieve your Content DNA. Please try again.')
    fetchError.value = 'Could not retrieve your Content DNA. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => loadDNA())

// ── Helpers ──────────────────────────────────────────────────────────────────
const pct = (v) => Math.round((v ?? 0) * 100)

const formatAffinityBars = computed(() => {
  const fa = dnaData.value?.dna?.format_affinity ?? {}
  return [
    { label: 'Short Form', value: fa.short_form ?? 0, color: '#4DDCC6' },
    { label: 'Long Form', value: fa.long_form ?? 0, color: '#7C6FFF' },
  ]
})

const contentBiasBars = computed(() => {
  const cb = dnaData.value?.dna?.content_bias ?? {}
  return [
    { label: 'Education', value: cb.education ?? 0, color: '#4DDCC6' },
    { label: 'Entertainment', value: cb.entertainment ?? 0, color: '#F59E0B' },
    { label: 'Other', value: cb.other ?? 0, color: '#6B7280' },
  ]
})

const timeBars = computed(() => {
  const tp = dnaData.value?.dna?.time_performance ?? {}
  return [
    { label: 'Morning', value: tp.morning ?? 0, icon: 'wb_sunny', color: '#F59E0B' },
    { label: 'Afternoon', value: tp.afternoon ?? 0, icon: 'light_mode', color: '#F97316' },
    { label: 'Evening', value: tp.evening ?? 0, icon: 'nights_stay', color: '#4DDCC6' },
    { label: 'Night', value: tp.night ?? 0, icon: 'dark_mode', color: '#7C6FFF' },
  ]
})

const lengthBars = computed(() => {
  const lp = dnaData.value?.dna?.length_preference ?? {}
  return [
    { label: '0–60 sec', value: lp['0-60s'] ?? 0, color: '#4DDCC6' },
    { label: '1–3 min', value: lp['1-3min'] ?? 0, color: '#7C6FFF' },
    { label: '3 min+', value: lp['3min+'] ?? 0, color: '#F59E0B' },
  ]
})

const summaryCards = computed(() => {
  const s = dnaData.value?.summary ?? {}
  return [
    { label: 'Dominant Format', value: s.dominant_format?.replace('_', ' ') ?? '—', icon: 'play_circle', color: '#4DDCC6' },
    { label: 'Dominant Topic', value: s.dominant_topic ?? '—', icon: 'school', color: '#7C6FFF' },
    { label: 'Best Time Slot', value: s.best_time ?? '—', icon: 'schedule', color: '#F59E0B' },
    { label: 'Ideal Length', value: s.ideal_length ?? '—', icon: 'timer', color: '#F97316' },
  ]
})
</script>

<template>
  <div class="space-y-8 max-w-5xl mx-auto relative pb-16">

    <!-- Ambient glows -->
    <div class="absolute top-0 left-0 w-80 h-80 bg-[#7C6FFF]/5 rounded-full blur-[140px] pointer-events-none -z-10" />
    <div class="absolute bottom-0 right-0 w-80 h-80 bg-brand/5 rounded-full blur-[140px] pointer-events-none -z-10" />

    <!-- ── Header ─────────────────────────────────────────────────────── -->
    <div class="flex items-center justify-between">
      <div>
        <span class="text-xs text-brand font-semibold tracking-widest uppercase">Genetic Profile</span>
        <h2 class="text-2xl font-bold text-white tracking-tight mt-0.5">Content DNA</h2>
        <p class="text-sm text-gray-500 mt-1" v-if="dnaData">
          Generated {{ new Date(dnaData.generated_at).toLocaleDateString('en-US', { dateStyle: 'long' }) }}
        </p>
      </div>
      <button @click="loadDNA"
        class="flex items-center gap-2 px-4 py-2 bg-white/3 hover:bg-white/8 text-white text-sm font-medium rounded-xl border border-white/8 transition-all cursor-pointer">
        <span class="material-symbols-outlined text-lg" :class="{ 'animate-spin': isLoading }">refresh</span>
        Refresh
      </button>
    </div>

    <!-- ── Error ──────────────────────────────────────────────────────── -->
    <div v-if="fetchError"
      class="p-5 bg-red-500/10 border border-red-500/15 rounded-2xl flex items-center gap-3 text-red-200">
      <span class="material-symbols-outlined text-2xl shrink-0 text-red-400">error</span>
      <p class="text-sm grow">{{ fetchError }}</p>
      <button @click="loadDNA"
        class="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-xs font-semibold rounded-lg transition-all">Retry</button>
    </div>

    <!-- ── Skeleton ───────────────────────────────────────────────────── -->
    <div v-else-if="isLoading" class="space-y-6 animate-pulse">
      <div class="h-36 rounded-3xl bg-white/3 border border-white/4" />
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="h-28 rounded-2xl bg-white/3 border border-white/4" />
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="i in 4" :key="i" class="h-56 rounded-3xl bg-white/3 border border-white/4" />
      </div>
    </div>

    <!-- ── Main content ───────────────────────────────────────────────── -->
    <div v-else class="space-y-8">

      <!-- DNA Helix Hero Banner -->
      <div class="relative overflow-hidden rounded-3xl border border-white/6 bg-[#0e0e0e] p-8">
        <!-- decorative rings -->
        <div class="absolute -top-16 -right-16 w-64 h-64 rounded-full border border-brand/10 pointer-events-none" />
        <div class="absolute -top-8  -right-8  w-48 h-48 rounded-full border border-brand/10 pointer-events-none" />
        <div class="absolute -top-2  -right-2  w-36 h-36 rounded-full border border-brand/15 pointer-events-none" />
        <div
          class="absolute -bottom-16 -left-16 w-64 h-64 rounded-full border border-[#7C6FFF]/10 pointer-events-none" />
        <div
          class="absolute -bottom-8  -left-8  w-48 h-48 rounded-full border border-[#7C6FFF]/10 pointer-events-none" />

        <div class="relative z-10 flex flex-col md:flex-row md:items-center gap-8">
          <!-- Helix graphic -->
          <div class="shrink-0 flex items-center justify-center">
            <div class="relative w-24 h-24">
              <!-- outer spin ring -->
              <div
                class="absolute inset-0 rounded-full border-2 border-dashed border-brand/30 animate-spin [animation-duration:12s]" />
              <!-- mid ring -->
              <div
                class="absolute inset-3 rounded-full border border-[#7C6FFF]/40 animate-spin [animation-duration:8s] [animation-direction:reverse]" />
              <!-- core -->
              <div
                class="absolute inset-6 rounded-full bg-linear-to-br from-brand/30 to-[#7C6FFF]/30 flex items-center justify-center border border-brand/30">
                <span class="material-symbols-outlined text-brand text-xl">genetics</span>
              </div>
            </div>
          </div>

          <!-- Summary text -->
          <div class="flex-1">
            <div
              class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full border border-brand/25 bg-brand/10 text-xs font-semibold text-brand uppercase tracking-wider mb-3">
              <span class="material-symbols-outlined text-xs animate-pulse">auto_awesome</span>
              AI-Decoded Profile
            </div>
            <h3 class="text-xl md:text-2xl font-bold text-white leading-snug mb-2">
              Your content thrives as
              <span class="text-brand">{{ dnaData?.summary?.dominant_format?.replace('_', '-') }}</span>,
              education-driven, and performs best in
              <span class="text-[#F59E0B]">{{ dnaData?.summary?.best_time }}</span> slots.
            </h3>
            <p class="text-sm text-gray-400 leading-relaxed">
              This genetic fingerprint of your creative identity is built from historical performance data,
              audience engagement signals, and algorithmic pattern analysis.
            </p>
          </div>
        </div>
      </div>

      <!-- Summary Stat Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="card in summaryCards" :key="card.label"
          class="group bg-[#111111] border border-white/6 rounded-2xl p-5 flex flex-col gap-3 hover:border-white/12 transition-all duration-200">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center"
            :style="`background: ${card.color}18; border: 1px solid ${card.color}30`">
            <span class="material-symbols-outlined text-lg" :style="`color: ${card.color}`">{{ card.icon }}</span>
          </div>
          <div>
            <p class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold">{{ card.label }}</p>
            <p class="text-base font-bold text-white capitalize mt-0.5">{{ card.value }}</p>
          </div>
        </div>
      </div>

      <!-- Metric Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <!-- Format Affinity -->
        <div class="bg-[#111111] border border-white/6 rounded-3xl p-6 hover:border-white/10 transition-all">
          <div class="flex items-center gap-2.5 mb-5">
            <div class="w-8 h-8 rounded-xl bg-brand/10 border border-brand/20 flex items-center justify-center">
              <span class="material-symbols-outlined text-brand text-base">aspect_ratio</span>
            </div>
            <div>
              <h4 class="text-sm font-bold text-white">Format Affinity</h4>
              <p class="text-[11px] text-gray-500">Short vs long content tendency</p>
            </div>
          </div>
          <div class="space-y-4">
            <div v-for="bar in formatAffinityBars" :key="bar.label">
              <div class="flex justify-between items-center mb-1.5">
                <span class="text-xs font-medium text-gray-400">{{ bar.label }}</span>
                <span class="text-xs font-bold" :style="`color: ${bar.color}`">{{ pct(bar.value) }}%</span>
              </div>
              <div class="h-2.5 rounded-full bg-white/5 overflow-hidden">
                <div class="h-full rounded-full transition-all duration-1000 ease-out"
                  :style="`width: ${pct(bar.value)}%; background: linear-gradient(90deg, ${bar.color}99, ${bar.color})`" />
              </div>
            </div>
          </div>
          <!-- split visual -->
          <div class="mt-5 flex gap-2 h-3 rounded-full overflow-hidden">
            <div v-for="bar in formatAffinityBars" :key="bar.label + '-split'"
              class="h-full rounded-full transition-all duration-700"
              :style="`width: ${pct(bar.value)}%; background: ${bar.color}`" />
          </div>
        </div>

        <!-- Content Bias -->
        <div class="bg-[#111111] border border-white/6 rounded-3xl p-6 hover:border-white/10 transition-all">
          <div class="flex items-center gap-2.5 mb-5">
            <div class="w-8 h-8 rounded-xl bg-[#7C6FFF]/10 border border-[#7C6FFF]/20 flex items-center justify-center">
              <span class="material-symbols-outlined text-base" style="color:#7C6FFF">school</span>
            </div>
            <div>
              <h4 class="text-sm font-bold text-white">Content Bias</h4>
              <p class="text-[11px] text-gray-500">Topic distribution across your library</p>
            </div>
          </div>
          <div class="space-y-4">
            <div v-for="bar in contentBiasBars" :key="bar.label">
              <div class="flex justify-between items-center mb-1.5">
                <span class="text-xs font-medium text-gray-400">{{ bar.label }}</span>
                <span class="text-xs font-bold" :style="`color: ${bar.color}`">{{ pct(bar.value) }}%</span>
              </div>
              <div class="h-2.5 rounded-full bg-white/5 overflow-hidden">
                <div class="h-full rounded-full transition-all duration-1000 ease-out"
                  :style="`width: ${pct(bar.value)}%; background: linear-gradient(90deg, ${bar.color}99, ${bar.color})`" />
              </div>
            </div>
          </div>
          <!-- bubble indicators -->
          <div class="mt-5 flex gap-3">
            <div v-for="bar in contentBiasBars" :key="bar.label + '-dot'" class="flex items-center gap-1.5">
              <div class="w-2 h-2 rounded-full" :style="`background: ${bar.color}`" />
              <span class="text-[11px] text-gray-500">{{ bar.label }}</span>
            </div>
          </div>
        </div>

        <!-- Time Performance -->
        <div class="bg-[#111111] border border-white/6 rounded-3xl p-6 hover:border-white/10 transition-all">
          <div class="flex items-center gap-2.5 mb-5">
            <div class="w-8 h-8 rounded-xl bg-[#F59E0B]/10 border border-[#F59E0B]/20 flex items-center justify-center">
              <span class="material-symbols-outlined text-base" style="color:#F59E0B">schedule</span>
            </div>
            <div>
              <h4 class="text-sm font-bold text-white">Time Performance</h4>
              <p class="text-[11px] text-gray-500">Engagement score by time of day</p>
            </div>
          </div>
          <!-- Gauge bars -->
          <div class="space-y-3">
            <div v-for="bar in timeBars" :key="bar.label" class="flex items-center gap-3">
              <div class="w-8 h-8 shrink-0 rounded-lg flex items-center justify-center"
                :style="`background: ${bar.color}12; border: 1px solid ${bar.color}25`">
                <span class="material-symbols-outlined text-sm" :style="`color: ${bar.color}`">{{ bar.icon }}</span>
              </div>
              <div class="flex-1">
                <div class="flex justify-between mb-1">
                  <span class="text-[11px] text-gray-400 font-medium">{{ bar.label }}</span>
                  <span class="text-[11px] font-bold" :style="`color: ${bar.color}`">{{ pct(bar.value) }}%</span>
                </div>
                <div class="h-2 rounded-full bg-white/5 overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-1000 ease-out"
                    :style="`width: ${pct(bar.value)}%; background: ${bar.color}`" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Length Preference -->
        <div class="bg-[#111111] border border-white/6 rounded-3xl p-6 hover:border-white/10 transition-all">
          <div class="flex items-center gap-2.5 mb-5">
            <div class="w-8 h-8 rounded-xl bg-[#F97316]/10 border border-[#F97316]/20 flex items-center justify-center">
              <span class="material-symbols-outlined text-base" style="color:#F97316">timer</span>
            </div>
            <div>
              <h4 class="text-sm font-bold text-white">Length Preference</h4>
              <p class="text-[11px] text-gray-500">Audience-preferred content duration</p>
            </div>
          </div>

          <DashboardContentDnaLengthChart :bars="lengthBars" />
        </div>

      </div>

      <!-- DNA Strand Footer -->
      <div class="rounded-2xl border border-white/5 bg-[#0c0c0c] px-6 py-4 flex items-center gap-4">
        <span class="material-symbols-outlined text-gray-600 text-xl">info</span>
        <p class="text-xs text-gray-500 leading-relaxed">
          Content DNA is recalculated every 24 hours based on the last 90 days of performance. Scores reflect normalised
          engagement ratios, not raw view counts.
        </p>
      </div>

    </div>
  </div>
</template>
