<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const { apiFetch } = useApiFetch()

const insights = ref(null)
const isLoading = ref(true)
const fetchError = ref(null)

async function loadInsights() {
  isLoading.value = true
  fetchError.value = null
  try {
    const data = await apiFetch('/user/insights')
    insights.value = data
  } catch (err) {
    console.error('Failed to load insights:', err)
    fetchError.value = 'Failed to load strategy insights. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadInsights()
})
</script>

<template>
  <div class="space-y-8 max-w-5xl mx-auto relative pb-12">
    <!-- Ambient background glows -->
    <div class="absolute top-0 left-1/4 w-96 h-96 bg-brand/5 rounded-full blur-[120px] pointer-events-none -z-10" />
    <div
      class="absolute bottom-10 right-1/4 w-96 h-96 bg-brand/5 rounded-full blur-[120px] pointer-events-none -z-10" />

    <!-- Top Action Bar -->
    <div class="flex justify-between items-center">
      <div>
        <span class="text-xs text-brand font-semibold tracking-widest uppercase font-label-md">Creator
          Intelligence</span>
        <h2 class="text-2xl font-bold text-white tracking-tight">Overview</h2>
      </div>
      <button @click="loadInsights"
        class="flex items-center gap-2 px-4 py-2 bg-white/[0.03] hover:bg-white/[0.08] text-white text-sm font-medium rounded-xl border border-white/[0.08] transition-all cursor-pointer">
        <span class="material-symbols-outlined text-lg" :class="{ 'animate-spin': isLoading }">refresh</span>
        Refresh
      </button>
    </div>

    <!-- Error State -->
    <div v-if="fetchError"
      class="p-5 bg-red-500/10 border border-red-500/15 rounded-2xl flex items-center gap-3 text-red-200">
      <span class="material-symbols-outlined text-2xl flex-shrink-0 text-red-400">error</span>
      <div class="flex-grow">
        <p class="text-sm font-semibold">Error Loading Insights</p>
        <p class="text-xs text-gray-400 mt-0.5">{{ fetchError }}</p>
      </div>
      <button @click="loadInsights"
        class="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-xs font-semibold rounded-lg transition-all">Retry</button>
    </div>

    <!-- Loading State -->
    <div v-else-if="isLoading" class="space-y-8">
      <div class="h-64 bg-white/[0.02] border border-white/[0.04] rounded-3xl animate-pulse" />
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="i in 4" :key="i"
          class="h-44 bg-white/[0.02] border border-white/[0.04] rounded-3xl animate-pulse" />
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="space-y-8">
      <!-- Strategy Block Hero Card -->
      <div
        class="relative overflow-hidden bg-[#121212] border border-white/[0.06] rounded-3xl p-8 shadow-2xl transition-all duration-300 hover:border-brand/20">
        <!-- Radial glow -->
        <div class="absolute -right-24 -top-24 w-80 h-80 bg-brand/10 rounded-full blur-3xl pointer-events-none" />
        <div class="absolute -left-24 -bottom-24 w-80 h-80 bg-brand/5 rounded-full blur-3xl pointer-events-none" />

        <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div class="max-w-2xl">
            <div
              class="inline-flex items-center gap-1.5 px-3 py-1 border border-brand/25 rounded-full bg-brand/10 mb-4 text-xs font-semibold text-brand uppercase tracking-wider">
              <span class="material-symbols-outlined text-sm animate-pulse">auto_awesome</span> Core Content Strategy
            </div>
            <h3 class="text-2xl md:text-3xl font-bold text-white mb-4 leading-tight">
              {{ insights?.strategy_block?.strategy }}
            </h3>
            <p class="text-sm text-gray-400 leading-relaxed">
              Based on algorithmic behavior, audience retention profiles, and engagement data, this recommended channel
              strategy is optimized for your target community.
            </p>
          </div>

          <!-- Large abstract visualization -->
          <div
            class="flex-shrink-0 flex items-center justify-center w-36 h-36 rounded-full bg-gradient-to-tr from-brand/20 to-brand/5 border border-brand/30 shadow-[0_0_30px_rgba(77,220,198,0.1)] relative">
            <div
              class="absolute inset-2 rounded-full border border-dashed border-brand/20 animate-spin [animation-duration:15s]" />
            <span class="material-symbols-outlined text-5xl text-brand">track_changes</span>
          </div>
        </div>
      </div>

      <!-- Strategy Parameters Bento Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <!-- Parameter 1: Best Content Type -->
        <div
          class="group bg-[#121212] border border-white/[0.06] rounded-3xl p-6 transition-all duration-300 hover:border-brand/20 hover:bg-[#141414] flex flex-col justify-between min-h-[180px]">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[10px] text-brand font-bold uppercase tracking-wider block mb-1">Optimal Format</span>
              <h4 class="text-lg font-bold text-white mb-2">Content Type</h4>
            </div>
            <div
              class="w-10 h-10 rounded-2xl bg-brand/10 border border-brand/20 flex items-center justify-center text-brand transition-transform group-hover:scale-110">
              <span class="material-symbols-outlined text-xl">smart_display</span>
            </div>
          </div>

          <div class="mt-4">
            <span class="text-2xl font-bold text-white block capitalize tracking-tight">{{
              insights?.strategy_block?.best_content_type }}</span>
            <div class="flex items-center gap-1.5 text-[11px] text-gray-500 mt-2">
              <span class="material-symbols-outlined text-xs">info</span>
              Standardized for maximum retention.
            </div>
          </div>
        </div>

        <!-- Parameter 2: Best Topic -->
        <div
          class="group bg-[#121212] border border-white/[0.06] rounded-3xl p-6 transition-all duration-300 hover:border-brand/20 hover:bg-[#141414] flex flex-col justify-between min-h-[180px]">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[10px] text-brand font-bold uppercase tracking-wider block mb-1">Niche Target</span>
              <h4 class="text-lg font-bold text-white mb-2">Best Topic</h4>
            </div>
            <div
              class="w-10 h-10 rounded-2xl bg-brand/10 border border-brand/20 flex items-center justify-center text-brand transition-transform group-hover:scale-110">
              <span class="material-symbols-outlined text-xl">tag</span>
            </div>
          </div>

          <div class="mt-4">
            <span class="text-2xl font-bold text-white block capitalize tracking-tight">{{
              insights?.strategy_block?.best_topic }}</span>
            <div class="flex items-center gap-1.5 text-[11px] text-gray-500 mt-2">
              <span class="material-symbols-outlined text-xs">info</span>
              Highly aligned with current user search queries.
            </div>
          </div>
        </div>

        <!-- Parameter 3: Best Posting Time -->
        <div
          class="group bg-[#121212] border border-white/[0.06] rounded-3xl p-6 transition-all duration-300 hover:border-brand/20 hover:bg-[#141414] flex flex-col justify-between min-h-[180px]">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[10px] text-brand font-bold uppercase tracking-wider block mb-1">Timing Matrix</span>
              <h4 class="text-lg font-bold text-white mb-2">Ideal Posting Hours</h4>
            </div>
            <div
              class="w-10 h-10 rounded-2xl bg-brand/10 border border-brand/20 flex items-center justify-center text-brand transition-transform group-hover:scale-110">
              <span class="material-symbols-outlined text-xl">alarm_on</span>
            </div>
          </div>

          <div class="mt-4">
            <span class="text-2xl font-bold text-white block tracking-tight">{{
              insights?.strategy_block?.best_posting_time }}</span>
            <div class="flex items-center gap-1.5 text-[11px] text-gray-500 mt-2">
              <span class="material-symbols-outlined text-xs">info</span>
              Peak audience availability window.
            </div>
          </div>
        </div>

        <!-- Parameter 4: Best Duration -->
        <div
          class="group bg-[#121212] border border-white/[0.06] rounded-3xl p-6 transition-all duration-300 hover:border-brand/20 hover:bg-[#141414] flex flex-col justify-between min-h-[180px]">
          <div class="flex justify-between items-start">
            <div>
              <span class="text-[10px] text-brand font-bold uppercase tracking-wider block mb-1">Attention Span</span>
              <h4 class="text-lg font-bold text-white mb-2">Recommended Duration</h4>
            </div>
            <div
              class="w-10 h-10 rounded-2xl bg-brand/10 border border-brand/20 flex items-center justify-center text-brand transition-transform group-hover:scale-110">
              <span class="material-symbols-outlined text-xl">timelapse</span>
            </div>
          </div>

          <div class="mt-4">
            <span class="text-2xl font-bold text-white block tracking-tight">{{ insights?.strategy_block?.best_duration
            }}</span>
            <div class="flex items-center gap-1.5 text-[11px] text-gray-500 mt-2">
              <span class="material-symbols-outlined text-xs">info</span>
              Optimized for full completion metrics.
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>
