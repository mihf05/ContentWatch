<script setup>
definePageMeta({ middleware: 'auth' })

useHead({ title: 'Dashboard — ContentWatch' })

const authStore = useAuthStore()
const { showPopup } = usePopup()

// State
const ytConnected = ref(false)
const ttConnected = ref(false)

const isAnalyzing = ref(false)
const analysisProgress = ref(0)
const analysisStep = ref('')
const hasAnalyzed = ref(false)

// Simulated OAuth Flow
function connectPlatform(platform) {
  const name = platform === 'youtube' ? 'YouTube' : 'TikTok'
  if (platform === 'youtube') {
    ytConnected.value = true
  } else {
    ttConnected.value = true
  }
  showPopup(`Connected ${name} account successfully!`)
}

function disconnectPlatform(platform) {
  const name = platform === 'youtube' ? 'YouTube' : 'TikTok'
  if (platform === 'youtube') {
    ytConnected.value = false
  } else {
    ttConnected.value = false
  }
  showPopup(`Disconnected ${name} account.`)
}

// Simulated 7-Point AI Engine Analysis Run
const steps = [
  'Verifying API integration credentials...',
  'Extracting recent post metrics (views, likes, comments)...',
  'Initializing Retention Mapping algorithms...',
  'Processing comment threads for Sentiment Resonance...',
  'Calculating Velocity Tracking metrics & viral curves...',
  'Synthesizing audience Content DNA profile...',
  'Generating strategic next actions & optimal configurations...'
]

async function runAnalysis() {
  if (!ytConnected.value && !ttConnected.value) {
    showPopup('Please connect at least one platform to analyze.', 'error')
    return
  }

  isAnalyzing.value = true
  hasAnalyzed.value = false
  analysisProgress.value = 0

  for (let i = 0; i < steps.length; i++) {
    analysisStep.value = steps[i]
    analysisProgress.value = Math.round(((i + 1) / steps.length) * 100)
    await new Promise(resolve => setTimeout(resolve, 800)) // delay to simulate
  }

  isAnalyzing.value = false
  hasAnalyzed.value = true
  showPopup('Analysis completed! Your insights have been updated.')
}
</script>

<template>
  <main class="flex-grow pt-24 md:pt-32 pb-16 md:pb-24 relative z-10 px-4 sm:px-6 md:px-12 max-w-screen-2xl mx-auto w-full">
    <!-- Hero Glow background -->
    <div class="hero-glow"></div>

    <!-- Header info -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-10 relative z-10">
      <div>
        <h1 class="text-3xl font-bold text-white mb-2">Creator Hub</h1>
        <p class="text-gray-400 text-sm">Welcome back, <span class="text-brand font-medium">{{ authStore.user?.email }}</span></p>
      </div>

      <!-- Quick Status -->
      <div class="flex gap-3">
        <span class="px-3.5 py-1.5 rounded-full text-xs font-semibold bg-white/5 border border-white/10 text-gray-300 flex items-center gap-1.5">
          <span class="h-2 w-2 rounded-full" :class="ytConnected || ttConnected ? 'bg-brand shadow-[0_0_8px_#4ddcc6]' : 'bg-gray-500'"></span>
          {{ ytConnected || ttConnected ? 'Data Sync Active' : 'No Channels Connected' }}
        </span>
      </div>
    </div>

    <!-- Main Grid Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 relative z-10">
      
      <!-- Left side: Integrations & Run panel -->
      <div class="lg:col-span-4 flex flex-col gap-6">
        
        <!-- Platform Connections Card -->
        <div class="glass-card rounded-2xl p-6">
          <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">
            <Icon name="material-symbols:account-circle" class="text-brand text-xl" />
            Integrations
          </h2>

          <div class="flex flex-col gap-4">
            <!-- YouTube Connection -->
            <div class="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5 hover:border-white/10 transition-colors">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-[#FF0000]/10 flex items-center justify-center border border-[#FF0000]/20">
                  <Icon name="logos:youtube-icon" class="text-xl" />
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white">YouTube</h3>
                  <p class="text-xs text-gray-400">{{ ytConnected ? 'Channel Synced' : 'Not Connected' }}</p>
                </div>
              </div>
              <button 
                @click="ytConnected ? disconnectPlatform('youtube') : connectPlatform('youtube')"
                :disabled="isAnalyzing"
                class="px-4 py-1.5 text-xs font-bold rounded-lg border transition-all"
                :class="ytConnected 
                  ? 'border-white/10 text-gray-400 hover:bg-white/5' 
                  : 'border-brand/30 bg-brand/10 text-brand hover:bg-brand/20'"
              >
                {{ ytConnected ? 'Disconnect' : 'Connect' }}
              </button>
            </div>

            <!-- TikTok Connection -->
            <div class="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5 hover:border-white/10 transition-colors">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-black flex items-center justify-center border border-white/10">
                  <Icon name="logos:tiktok-icon" class="text-xl" />
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white">TikTok</h3>
                  <p class="text-xs text-gray-400">{{ ttConnected ? 'Channel Synced' : 'Not Connected' }}</p>
                </div>
              </div>
              <button 
                @click="ttConnected ? disconnectPlatform('tiktok') : connectPlatform('tiktok')"
                :disabled="isAnalyzing"
                class="px-4 py-1.5 text-xs font-bold rounded-lg border transition-all"
                :class="ttConnected 
                  ? 'border-white/10 text-gray-400 hover:bg-white/5' 
                  : 'border-brand/30 bg-brand/10 text-brand hover:bg-brand/20'"
              >
                {{ ttConnected ? 'Disconnect' : 'Connect' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 7-Point AI Engine trigger -->
        <div class="glass-card rounded-2xl p-6">
          <h2 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
            <Icon name="material-symbols:auto-awesome" class="text-brand text-xl" />
            7-Point AI Analysis
          </h2>
          <p class="text-gray-400 text-xs mb-6">
            Run the core intelligence model across connected platforms to map retention, sentiment, and content DNA.
          </p>

          <button 
            @click="runAnalysis"
            :disabled="isAnalyzing || (!ytConnected && !ttConnected)"
            class="w-full bg-brand text-jetblack font-bold text-sm py-3.5 rounded-xl hover:shadow-[0_0_20px_rgba(77,220,198,0.35)] transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <span v-if="isAnalyzing" class="inline-block animate-spin rounded-full h-4 w-4 border-2 border-current border-t-transparent" role="status"></span>
            {{ isAnalyzing ? 'Running Engine...' : 'Analyze Channel' }}
          </button>

          <!-- Loader progress details -->
          <div v-if="isAnalyzing" class="mt-6 p-4 bg-white/5 border border-white/10 rounded-xl">
            <div class="flex justify-between items-center text-xs text-gray-300 mb-2">
              <span class="font-medium">Model Inference</span>
              <span class="font-bold text-brand">{{ analysisProgress }}%</span>
            </div>
            <!-- Progress Bar -->
            <div class="w-full h-1.5 bg-white/10 rounded-full overflow-hidden mb-3">
              <div class="h-full bg-brand transition-all duration-300" :style="{ width: `${analysisProgress}%` }"></div>
            </div>
            <p class="text-[11px] text-gray-400 animate-pulse">{{ analysisStep }}</p>
          </div>
        </div>

      </div>

      <!-- Right side: Insights Visualization Panel -->
      <div class="lg:col-span-8">
        
        <!-- Placeholder Empty State -->
        <div v-if="!isAnalyzing && !hasAnalyzed" class="glass-card rounded-2xl p-12 text-center flex flex-col items-center justify-center min-h-[480px]">
          <div class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center border border-white/10 mb-6 text-brand">
            <Icon name="material-symbols:insights-outline" class="text-3xl" />
          </div>
          <h2 class="text-xl font-bold text-white mb-2">Awaiting Intelligence Run</h2>
          <p class="text-gray-400 text-sm max-w-sm mx-auto mb-6">
            Connect your YouTube/TikTok channels and trigger the 7-Point AI Engine to generate strategy reports.
          </p>
          <div class="flex items-center gap-2 text-xs text-gray-500">
            <Icon name="material-symbols:lock" />
            <span>Secure SSL Encryption Enabled</span>
          </div>
        </div>

        <!-- Progress Placeholder while analyzing -->
        <div v-else-if="isAnalyzing" class="glass-card rounded-2xl p-12 text-center flex flex-col items-center justify-center min-h-[480px]">
          <div class="relative w-20 h-20 mb-6 flex items-center justify-center">
            <div class="absolute inset-0 rounded-full border-4 border-white/5"></div>
            <div class="absolute inset-0 rounded-full border-4 border-brand border-t-transparent animate-spin"></div>
            <Icon name="material-symbols:auto-awesome" class="text-brand text-2xl animate-pulse" />
          </div>
          <h2 class="text-xl font-bold text-white mb-2">Analyzing Channel Data</h2>
          <p class="text-gray-400 text-sm max-w-sm mx-auto mb-4">
            Our multi-point algorithms are scanning recent upload performance and cataloging viewer behaviors.
          </p>
          <span class="text-xs bg-brand/10 border border-brand/20 text-brand px-3 py-1 rounded-full font-medium">
            {{ analysisProgress }}% Complete
          </span>
        </div>

        <!-- Premium Real Simulated Insights Dashboard -->
        <div v-else-if="hasAnalyzed" class="flex flex-col gap-6 animate-fade-in">
          
          <!-- Bento Grid stats -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Optimal Format -->
            <div class="glass-card rounded-2xl p-5 border-t-2 border-t-brand">
              <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-4">Best Format</span>
              <div class="text-2xl font-bold text-white mb-1">Short-Form</div>
              <span class="text-xs text-brand flex items-center gap-1 font-semibold">
                <Icon name="material-symbols:trending-up" /> +28% Engagement Affinity
              </span>
            </div>

            <!-- Posting Schedule -->
            <div class="glass-card rounded-2xl p-5">
              <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-4">Ideal Post Time</span>
              <div class="text-2xl font-bold text-white mb-1">6:00 PM EST</div>
              <span class="text-xs text-gray-400 font-semibold">
                Thursdays & Saturdays
              </span>
            </div>

            <!-- Content Length -->
            <div class="glass-card rounded-2xl p-5">
              <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-4">Ideal Duration</span>
              <div class="text-2xl font-bold text-white mb-1">45 - 60s</div>
              <span class="text-xs text-brand flex items-center gap-1 font-semibold">
                <Icon name="material-symbols:check-circle" /> Optimized Retention
              </span>
            </div>
          </div>

          <!-- Retention Strategy & Action Items -->
          <div class="glass-card rounded-2xl p-6">
            <h2 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <Icon name="material-symbols:bolt" class="text-brand text-xl" />
              Strategic Recommendations
            </h2>

            <div class="flex flex-col gap-4">
              <!-- Item 1 -->
              <div class="p-4 bg-white/5 rounded-xl border border-white/5 flex gap-4">
                <div class="w-8 h-8 rounded-lg bg-brand/10 flex items-center justify-center text-brand flex-shrink-0">
                  <span class="font-bold text-sm">1</span>
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white mb-1">Hook Optimization</h3>
                  <p class="text-xs text-gray-400 leading-relaxed">
                    Retain 15% more viewers by reducing intro animations. Ensure visual pattern interrupts occur in the first 3 seconds.
                  </p>
                </div>
              </div>

              <!-- Item 2 -->
              <div class="p-4 bg-white/5 rounded-xl border border-white/5 flex gap-4">
                <div class="w-8 h-8 rounded-lg bg-brand/10 flex items-center justify-center text-brand flex-shrink-0">
                  <span class="font-bold text-sm">2</span>
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white mb-1">Topic Clustering</h3>
                  <p class="text-xs text-gray-400 leading-relaxed">
                    Prioritize topics covering <strong class="text-white">Sustainable Tech</strong> and <strong class="text-white">Smart Hardware</strong>. These topics currently yield a 2.4x higher comment density.
                  </p>
                </div>
              </div>

              <!-- Item 3 -->
              <div class="p-4 bg-white/5 rounded-xl border border-white/5 flex gap-4">
                <div class="w-8 h-8 rounded-lg bg-brand/10 flex items-center justify-center text-brand flex-shrink-0">
                  <span class="font-bold text-sm">3</span>
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white mb-1">Engagement Velocity</h3>
                  <p class="text-xs text-gray-400 leading-relaxed">
                    Reply to comments containing questions within 60 minutes of posting. This triggers the algorithm's second-wave feed distribution.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Content DNA Profile -->
          <div class="glass-card rounded-2xl p-6">
            <h2 class="text-lg font-bold text-white mb-6 flex items-center gap-2">
              <Icon name="material-symbols:hub" class="text-brand text-xl" />
              Audience DNA Match
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <!-- DNA Stats -->
              <div class="flex flex-col gap-5 justify-center">
                <div>
                  <div class="flex justify-between text-xs font-semibold mb-1 text-gray-300">
                    <span>Education / Informative</span>
                    <span class="text-brand">85%</span>
                  </div>
                  <div class="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                    <div class="h-full bg-brand" style="width: 85%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between text-xs font-semibold mb-1 text-gray-300">
                    <span>Entertainment / Drama</span>
                    <span class="text-brand">40%</span>
                  </div>
                  <div class="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                    <div class="h-full bg-brand opacity-60" style="width: 40%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between text-xs font-semibold mb-1 text-gray-300">
                    <span>Community / Interactive</span>
                    <span class="text-brand">65%</span>
                  </div>
                  <div class="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                    <div class="h-full bg-brand opacity-80" style="width: 65%"></div>
                  </div>
                </div>
              </div>

              <!-- Extra Summary Info -->
              <div class="bg-white/5 border border-white/10 rounded-xl p-5 flex flex-col justify-between">
                <div>
                  <h3 class="text-sm font-semibold text-white mb-2">Audience Persona</h3>
                  <p class="text-xs text-gray-400 leading-relaxed mb-4">
                    Your viewers are highly analytical learners who seek structured insights but value concise, fast-paced editing.
                  </p>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-500 border-t border-white/5 pt-3">
                  <span>Confidence Index</span>
                  <span class="text-brand font-bold flex items-center gap-1">
                    <Icon name="material-symbols:verified" /> 94.2%
                  </span>
                </div>
              </div>
            </div>
          </div>

        </div>

      </div>

    </div>
  </main>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
