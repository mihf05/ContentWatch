<script setup>
const authStore = useAuthStore()

if (!authStore.user) {
  await authStore.fetchUser()
}
</script>

<template>
  <main
    class="flex-grow pt-24 md:pt-32 pb-16 md:pb-24 relative z-10 px-4 sm:px-6 md:px-12 max-w-screen-2xl mx-auto w-full overflow-hidden">
    <div class="hero-glow"></div>

    <!-- Hero Section -->
    <section id="solutions" class="text-center max-w-4xl mx-auto mb-16 md:mb-32 relative z-10 pt-6 md:pt-10">
      <div
        class="inline-block px-3 py-1.5 sm:px-4 sm:py-2 border border-brand/20 rounded-full bg-brand/10 mb-4 md:mb-6 font-label-md text-label-md text-brand">
        <Icon name="material-symbols:auto-awesome" class="text-[14px] align-middle mr-1" /> Intelligent Insight Engine
      </div>
      <h1 class="font-display-lg text-display-lg text-white mb-4 md:mb-6 px-2">
        Stop Guessing.<br />Start <span class="text-brand">Growing.</span>
      </h1>
      <p class="font-body-lg text-body-lg text-gray-400 mb-8 md:mb-10 max-w-2xl mx-auto px-2">
        AI-Driven Creator Intelligence that analyzes your audience's deepest engagement patterns to deliver precise,
        actionable content strategies.
      </p>
      <div class="flex justify-center">
        <NuxtLink to="/login"
          class="bg-brand text-jetblack font-label-md text-label-md px-6 sm:px-10 py-3 rounded-full hover:shadow-[0_0_20px_rgba(77,220,198,0.5)] transition-all flex items-center gap-2 font-bold text-sm sm:text-label-md">
          Analyze My Channel
          <Icon name="material-symbols:arrow-forward" class="text-[18px]" />
        </NuxtLink>
      </div>
    </section>

    <!-- Analytics Dashboard Section (Bento Grid) -->
    <section id="analytics" class="mb-16 md:mb-32 relative z-10 pt-20 -mt-20">
      <div class="flex flex-col md:flex-row md:items-center gap-3 md:gap-4 mb-8 md:mb-10">
        <h2 class="font-headline-lg text-headline-lg text-white">Precision Insights</h2>
        <div class="hidden md:block h-[1px] flex-grow bg-gradient-to-r from-white/10 to-transparent ml-6"></div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-4 sm:gap-6">
        <!-- Widget 1: Best Format -->
        <div
          class="sm:col-span-1 lg:col-span-4 glass-card rounded-xl p-5 sm:p-6 flex flex-col justify-between hover:bg-neutral-900 transition-colors duration-300 min-h-[180px]">
          <div class="flex justify-between items-start mb-6 sm:mb-10">
            <div class="font-label-md text-label-md text-gray-400 uppercase tracking-wider">Best Format</div>
            <Icon name="material-symbols:play-circle" class="text-brand text-2xl" />
          </div>
          <div>
            <div class="text-3xl md:text-display-lg md:font-display-lg font-bold text-white mb-1">Short-form</div>
            <div class="font-body-sm text-body-sm text-brand flex items-center gap-1">
              <Icon name="material-symbols:trending-up" class="text-[16px]" /> +24% Engagement
            </div>
          </div>
        </div>

        <!-- Widget 2: Top Cluster -->
        <div
          class="sm:col-span-1 lg:col-span-4 glass-card rounded-xl p-5 sm:p-6 flex flex-col justify-between hover:bg-neutral-900 transition-colors duration-300 min-h-[180px]">
          <div class="flex justify-between items-start mb-6 sm:mb-10">
            <div class="font-label-md text-label-md text-gray-400 uppercase tracking-wider">Top Cluster</div>
            <Icon name="material-symbols:hub" class="text-brand text-2xl" />
          </div>
          <div>
            <div class="font-headline-md text-headline-md text-white mb-2">Sustainable Tech</div>
            <div class="flex flex-wrap gap-2 mt-3">
              <span
                class="px-3 py-1 rounded-full bg-white/10 text-white font-label-md text-label-md border border-white/10">EVs</span>
              <span
                class="px-3 py-1 rounded-full bg-white/10 text-white font-label-md text-label-md border border-white/10">Solar</span>
            </div>
          </div>
        </div>

        <!-- Widget 3: Action Recommendation -->
        <div
          class="sm:col-span-2 lg:col-span-4 glass-card rounded-xl p-5 sm:p-6 flex flex-col hover:bg-neutral-900 transition-colors duration-300 border-t-2 border-t-brand relative overflow-hidden">
          <div class="absolute -right-4 -top-4 w-24 h-24 bg-brand/10 rounded-full blur-xl"></div>
          <div
            class="font-label-md text-label-md text-brand uppercase tracking-wider mb-4 sm:mb-6 flex items-center gap-2">
            <Icon name="material-symbols:bolt" class="text-[16px]" /> Next Action
          </div>
          <h3 class="font-headline-md text-headline-md text-white mb-3 sm:mb-4">Engage Fast</h3>
          <p class="font-body-sm text-body-sm text-gray-400 flex-grow">
            Reply to the top 3 comments within the first hour of posting to boost algorithmic reach by an estimated 18%.
          </p>
          <button
            class="mt-4 sm:mt-6 w-full py-2 border border-white/10 rounded-lg font-label-md text-label-md text-white hover:bg-white/5 transition-colors">
            View Details
          </button>
        </div>

        <!-- Widget 4: Optimal Post Time -->
        <div
          class="sm:col-span-1 lg:col-span-6 glass-card rounded-xl p-5 sm:p-6 flex items-center gap-4 sm:gap-6 hover:bg-neutral-900 transition-colors duration-300">
          <div
            class="w-10 h-10 sm:w-12 sm:h-12 rounded-full flex-shrink-0 bg-neutral-900 flex items-center justify-center border border-white/10">
            <Icon name="material-symbols:schedule" class="text-brand text-lg sm:text-xl" />
          </div>
          <div class="min-w-0">
            <div class="font-label-md text-label-md text-gray-400 uppercase tracking-wider mb-1">Optimal Time</div>
            <div class="font-numeric-data text-numeric-data text-brand truncate">6:00 PM EST <span
                class="text-gray-400 text-[13px] sm:text-[14px] ml-1 sm:ml-2 font-body-sm">Thursdays</span></div>
          </div>
        </div>

        <!-- Widget 5: Ideal Content Length -->
        <div
          class="sm:col-span-1 lg:col-span-6 glass-card rounded-xl p-5 sm:p-6 flex items-center gap-4 sm:gap-6 hover:bg-neutral-900 transition-colors duration-300">
          <div
            class="w-10 h-10 sm:w-12 sm:h-12 rounded-full flex-shrink-0 bg-neutral-900 flex items-center justify-center border border-white/10">
            <Icon name="material-symbols:timer" class="text-brand text-lg sm:text-xl" />
          </div>
          <div class="min-w-0">
            <div class="font-label-md text-label-md text-gray-400 uppercase tracking-wider mb-1">Ideal Length</div>
            <div class="font-numeric-data text-numeric-data text-brand">45-60 seconds</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Core System Features -->
    <section id="features" class="relative z-10 pt-20 -mt-20">
      <div class="text-center mb-8 md:mb-10 pt-10 md:pt-16 border-t border-white/5">
        <h2 class="font-headline-lg text-headline-lg text-white mb-3 md:mb-4">The 7-Point Engine</h2>
        <p class="font-body-md text-body-md text-gray-400 max-w-2xl mx-auto px-2">
          Our proprietary model synthesizes seven distinct data streams to eliminate guesswork from your content
          strategy.
        </p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div
          class="p-5 sm:p-6 border border-white/5 rounded-xl bg-neutral-900/50 hover:border-white/10 hover:bg-neutral-900 transition-colors">
          <Icon name="material-symbols:visibility" class="text-brand mb-3 sm:mb-4 text-2xl sm:text-3xl" />
          <h4 class="font-headline-md text-[16px] sm:text-[18px] text-white mb-2 font-semibold">Retention Mapping</h4>
          <p class="font-body-sm text-body-sm text-gray-400">Analyzes exact drop-off points to suggest tighter editing
            strategies.</p>
        </div>
        <div
          class="p-5 sm:p-6 border border-white/5 rounded-xl bg-neutral-900/50 hover:border-white/10 hover:bg-neutral-900 transition-colors">
          <Icon name="material-symbols:forum" class="text-brand mb-3 sm:mb-4 text-2xl sm:text-3xl" />
          <h4 class="font-headline-md text-[16px] sm:text-[18px] text-white mb-2 font-semibold">Sentiment Analysis</h4>
          <p class="font-body-sm text-body-sm text-gray-400">Classifies comment sentiment to gauge true audience
            resonance.</p>
        </div>
        <div
          class="p-5 sm:p-6 border border-white/5 rounded-xl bg-neutral-900/50 hover:border-white/10 hover:bg-neutral-900 transition-colors sm:col-span-2 lg:col-span-1">
          <Icon name="material-symbols:share" class="text-brand mb-3 sm:mb-4 text-2xl sm:text-3xl" />
          <h4 class="font-headline-md text-[16px] sm:text-[18px] text-white mb-2 font-semibold">Velocity Tracking</h4>
          <p class="font-body-sm text-body-sm text-gray-400">Monitors initial share momentum to predict viral potential.
          </p>
        </div>
      </div>
    </section>
  </main>
</template>