<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})
</script>

<template>
  <div class="space-y-6 max-w-6xl mx-auto">
    <div>
      <h2 class="text-2xl font-bold text-white tracking-tight">Analytics</h2>
      <p class="text-sm text-gray-400">Detailed performance charts and telemetry data.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-[#141414] border border-white/[0.06] rounded-2xl p-6 h-64 flex flex-col justify-between">
        <div>
          <h3 class="text-base font-bold text-white mb-1">Audience Demographics</h3>
          <p class="text-xs text-gray-500">Location, age distribution and device usage statistics.</p>
        </div>
        <div class="flex items-center justify-center flex-grow text-gray-500 text-sm">
          <span class="material-symbols-outlined text-3xl mr-2 text-brand">bar_chart</span>
          Interactive demographics data will appear here.
        </div>
      </div>

      <div class="bg-[#141414] border border-white/[0.06] rounded-2xl p-6 h-64 flex flex-col justify-between">
        <div>
          <h3 class="text-base font-bold text-white mb-1">Traffic Sources</h3>
          <p class="text-xs text-gray-500">Direct, organic search, referral and social media traffic.</p>
        </div>
        <div class="flex items-center justify-center flex-grow text-gray-500 text-sm">
          <span class="material-symbols-outlined text-3xl mr-2 text-brand">pie_chart</span>
          Traffic distribution analytics will appear here.
        </div>
      </div>
    </div>
  </div>
</template>
