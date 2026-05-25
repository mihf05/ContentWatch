<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const platforms = [
  {
    name: 'YouTube',
    svgPath: 'M23.498 6.163a3.003 3.003 0 0 0-2.11-2.11C19.517 3.545 12 3.545 12 3.545s-7.516 0-9.387.507a3.003 3.003 0 0 0-2.11 2.11C0 8.033 0 12 0 12s0 3.967.502 5.837a3.003 3.003 0 0 0 2.11 2.11c1.871.507 9.386.507 9.386.507s7.517 0 9.387-.507a3.003 3.003 0 0 0 2.11-2.11C24 15.967 24 12 24 12s0-3.967-.502-5.837zM9.545 15.568V8.432L15.818 12l-6.273 3.568z',
    color: 'text-red-500 fill-current',
    desc: 'Fetch video views, likes, and comment logs.'
  },
  {
    name: 'TikTok',
    svgPath: 'M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.02 1.59 4.23a7.42 7.42 0 0 0 4.13 2.64v3.85a11.19 11.19 0 0 1-5.69-1.92v6.62c.04 3.08-1.57 5.92-4.24 7.45a8.77 8.77 0 0 1-9.15-.09C.46 21.28-1.01 17.88-.6 14.54c.46-3.8 3.5-6.84 7.3-7.3a8.96 8.96 0 0 1 5.82 1.48V.02z',
    color: 'text-white fill-current',
    desc: 'Sync videos, watch time metrics, and shares.'
  },
  {
    name: 'Instagram',
    svgPath: 'M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.051c-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a3.838 3.838 0 1 1 0-7.676A3.838 3.838 0 0 1 12 16zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z',
    color: 'text-pink-500 fill-current',
    desc: 'Pull reels performance and story insights.'
  }
]
</script>

<template>
  <div class="space-y-6 max-w-6xl mx-auto">
    <div>
      <h2 class="text-2xl font-bold text-white tracking-tight">Integrations</h2>
      <p class="text-sm text-gray-400">Connect ContentWatch with your creator profiles and third-party developer
        platforms.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="platform in platforms" :key="platform.name"
        class="bg-[#141414] border border-white/[0.06] rounded-2xl p-6 flex flex-col justify-between h-48">
        <div>
          <div class="flex items-center gap-2.5 mb-3">
            <svg class="w-6 h-6" :class="platform.color" viewBox="0 0 24 24">
              <path :d="platform.svgPath" />
            </svg>
            <h3 class="text-base font-bold text-white">{{ platform.name }}</h3>
          </div>
          <p class="text-xs text-gray-400 leading-relaxed">{{ platform.desc }}</p>
        </div>
        <button
          class="w-full py-2 bg-white/[0.04] hover:bg-white/[0.08] text-white text-xs font-semibold rounded-xl border border-white/[0.08] transition-all">
          Connect Account
        </button>
      </div>
    </div>
  </div>
</template>
