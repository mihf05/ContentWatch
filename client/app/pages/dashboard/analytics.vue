<script setup>
definePageMeta({
  layout: 'dashboard',
  middleware: 'auth',
})

useHead({ title: 'Analytics' })

const {
  isLoading,
  fetchError,
  loadAnalytics,
  viewsChart,
  engagementChart,
  contentTypeChart,
  durationChart,
  timeChart,
} = useAnalytics()

onMounted(() => loadAnalytics())
</script>

<template>
  <div class="analytics-page">
    <div class="analytics-ambient analytics-ambient--brand" />
    <div class="analytics-ambient analytics-ambient--purple" />

    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 min-w-0">
      <div class="min-w-0">
        <span class="text-label-md text-brand uppercase">Performance Telemetry</span>
        <h2 class="text-headline-lg text-white tracking-tight mt-1">Analytics</h2>
        <p class="text-body-sm text-gray-500 mt-1">
          Views and engagement trends plus bucket breakdowns by content, duration, and time.
        </p>
      </div>
      <button type="button" class="analytics-btn-secondary self-start sm:self-auto" @click="loadAnalytics">
        <span class="material-symbols-outlined text-lg" :class="{ 'animate-spin': isLoading }">refresh</span>
        Refresh
      </button>
    </div>

    <div v-if="fetchError" class="analytics-error flex-wrap" role="alert">
      <span class="material-symbols-outlined text-2xl shrink-0 text-red-400">error</span>
      <p class="text-body-sm grow text-red-200">{{ fetchError }}</p>
      <button type="button" class="analytics-btn-danger" @click="loadAnalytics">Retry</button>
    </div>

    <!-- Timeseries -->
    <div class="min-w-0">
      <p class="analytics-section-label">Trends</p>
      <div class="grid grid-cols-1 gap-6 min-w-0">
        <DashboardApexChartPanel featured accent="brand" title="Views Over Time"
          description="Daily view counts across your connected content" icon="visibility" :loading="isLoading"
          :chart="viewsChart" type="area" :height="340" />
        <div class="grid grid-cols-1 gap-6 min-w-0">
          <DashboardApexChartPanel accent="purple" title="Engagement Over Time"
            description="Daily engagement rate trend" icon="favorite" :loading="isLoading" :chart="engagementChart"
            type="area" :height="300" />
        </div>
      </div>
    </div>

    <!-- Buckets -->
    <div class="min-w-0">
      <p class="analytics-section-label">Buckets</p>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 min-w-0">
        <DashboardApexChartPanel accent="brand" title="By Content Type"
          description="Avg views and engagement per format" icon="smart_display" :loading="isLoading"
          :chart="contentTypeChart" type="bar" :height="320" />
        <DashboardApexChartPanel accent="amber" title="By Time of Day"
          description="Avg views and engagement per posting window" icon="schedule" :loading="isLoading"
          :chart="timeChart" type="bar" :height="320" />
        <DashboardApexChartPanel panel-class="lg:col-span-2" accent="orange" title="By Duration"
          description="Avg engagement across video length ranges" icon="timelapse" :loading="isLoading"
          :chart="durationChart" type="bar" :height="300" />
      </div>
    </div>
  </div>
</template>
