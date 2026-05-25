import {
  buildViewsTimeSeries,
  buildEngagementTimeSeries,
  buildContentTypeBucketChart,
  buildDurationBucketChart,
  buildTimeBucketChart,
} from '~/utils/apexChartOptions'

export function useAnalytics() {
  const { apiFetch } = useApiFetch()
  const { showError } = usePopup()

  const isLoading = ref(true)
  const fetchError = ref(null)

  const viewsTimeSeries = ref(null)
  const engagementTimeSeries = ref(null)
  const contentTypeBuckets = ref(null)
  const durationBuckets = ref(null)
  const timeBuckets = ref(null)

  async function loadAnalytics() {
    isLoading.value = true
    fetchError.value = null

    try {
      const [views, engagements, contentType, duration, time] = await Promise.all([
        apiFetch('/user/timeseries/views'),
        apiFetch('/user/timeseries/engagements'),
        apiFetch('/user/bucket/contentype'),
        apiFetch('/user/bucket/duration'),
        apiFetch('/user/bucket/time'),
      ])

      viewsTimeSeries.value = views
      engagementTimeSeries.value = engagements
      contentTypeBuckets.value = contentType
      durationBuckets.value = duration
      timeBuckets.value = time
    } catch (err) {
      showError(err, 'Could not load analytics data. Please try again.')
      fetchError.value = 'Could not load analytics data. Please try again.'
    } finally {
      isLoading.value = false
    }
  }

  const viewsChart = computed(() => buildViewsTimeSeries(viewsTimeSeries.value))
  const engagementChart = computed(() => buildEngagementTimeSeries(engagementTimeSeries.value))
  const contentTypeChart = computed(() => buildContentTypeBucketChart(contentTypeBuckets.value))
  const durationChart = computed(() => buildDurationBucketChart(durationBuckets.value))
  const timeChart = computed(() => buildTimeBucketChart(timeBuckets.value))

  return {
    isLoading,
    fetchError,
    loadAnalytics,
    viewsChart,
    engagementChart,
    contentTypeChart,
    durationChart,
    timeChart,
  }
}
