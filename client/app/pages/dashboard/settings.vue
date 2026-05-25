<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const authStore = useAuthStore()
</script>

<template>
  <div class="space-y-6 max-w-6xl mx-auto">
    <div>
      <h2 class="text-2xl font-bold text-white tracking-tight">Settings</h2>
      <p class="text-sm text-gray-400">Configure profile, strategy preferences, and credentials.</p>
    </div>

    <div class="bg-[#141414] border border-white/[0.06] rounded-2xl p-6 divide-y divide-white/[0.06] space-y-6">
      <!-- Profile section -->
      <div class="pb-6">
        <h3 class="text-base font-bold text-white mb-2">Account Email</h3>
        <p class="text-xs text-gray-400 mb-4">Your current sign-in credentials.</p>
        <div class="flex items-center gap-3">
          <div
            class="w-10 h-10 rounded-full bg-brand/10 border border-brand/20 flex items-center justify-center text-brand text-sm font-bold">
            {{ authStore.user?.email?.charAt(0)?.toUpperCase() || 'U' }}
          </div>
          <div>
            <span class="text-sm font-semibold text-white block">{{ authStore.user?.email }}</span>
            <span class="text-[10px] text-gray-500">Free Tier Account</span>
          </div>
        </div>
      </div>

      <!-- Settings configuration -->
      <div class="pt-6">
        <h3 class="text-base font-bold text-white mb-2 font-semibold">Preferences</h3>
        <div class="space-y-4 mt-4">
          <label class="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" checked class="rounded border-white/10 bg-white/5 text-brand focus:ring-0" />
            <div>
              <span class="text-xs font-semibold text-white block">Email Alerts</span>
              <span class="text-[10px] text-gray-500">Receive weekly channel health insights.</span>
            </div>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>
