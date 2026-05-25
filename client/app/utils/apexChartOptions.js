import {
  CHART_COLORS,
  CHART_COLOR_SEQUENCE,
  CHART_UI,
  chartGradientFill,
  chartStrokeGlow,
} from '~/utils/chartTheme'
import { formatCompactNumber, formatLabel } from '~/utils/format'

function formatDateTick(val) {
  const d = new Date(val)
  return Number.isNaN(d.getTime())
    ? val
    : d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function enhancedTooltip(yFormatters = {}) {
  return {
    theme: 'dark',
    shared: true,
    intersect: false,
    style: { fontSize: '12px', fontFamily: 'Inter, sans-serif' },
    marker: { show: true },
    x: { show: true },
    y: typeof yFormatters === 'function'
      ? { formatter: yFormatters }
      : yFormatters,
    custom: undefined,
  }
}

/** ApexCharts toolbar fully off (hides top-right menu). */
const CHART_TOOLBAR_OFF = {
  show: false,
  autoSelected: 'none',
  tools: {
    download: false,
    selection: false,
    zoom: false,
    zoomin: false,
    zoomout: false,
    pan: false,
    reset: false,
    customIcons: [],
  },
}

function enhancedLegend() {
  return {
    show: true,
    position: 'top',
    horizontalAlign: 'right',
    offsetY: -4,
    fontSize: '12px',
    fontWeight: 500,
    labels: { colors: CHART_UI.legend },
    markers: {
      width: 8,
      height: 8,
      radius: 12,
      strokeWidth: 0,
    },
    itemMargin: { horizontal: 12 },
  }
}

export function createBaseChartOptions(overrides = {}) {
  return {
    chart: {
      fontFamily: 'Inter, sans-serif',
      background: 'transparent',
      width: '100%',
      redrawOnParentResize: true,
      toolbar: CHART_TOOLBAR_OFF,
      zoom: { enabled: false },
      foreColor: CHART_UI.label,
      animations: {
        enabled: true,
        easing: 'easeinout',
        speed: 900,
        animateGradually: { enabled: true, delay: 120 },
        dynamicAnimation: { enabled: true, speed: 400 },
      },
      dropShadow: {
        enabled: true,
        top: 4,
        left: 0,
        blur: 12,
        opacity: 0.12,
        color: CHART_COLORS.brand,
      },
    },
    grid: {
      borderColor: CHART_UI.grid,
      strokeDashArray: 3,
      padding: { top: 8, right: 4, bottom: 4, left: 4 },
      xaxis: { lines: { show: false } },
      yaxis: { lines: { show: true } },
      row: { colors: ['transparent', 'transparent'], opacity: 0 },
    },
    xaxis: {
      labels: {
        style: { colors: CHART_UI.label, fontSize: '11px', fontWeight: 500 },
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
      crosshairs: {
        show: true,
        stroke: { color: CHART_UI.crosshair, width: 1, dashArray: 4 },
      },
    },
    yaxis: {
      labels: {
        style: { colors: CHART_UI.label, fontSize: '11px', fontWeight: 500 },
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    legend: enhancedLegend(),
    tooltip: enhancedTooltip(),
    dataLabels: { enabled: false },
    states: {
      hover: { filter: { type: 'lighten', value: 0.04 } },
      active: { filter: { type: 'darken', value: 0.06 } },
    },
    ...overrides,
  }
}

function timeSeriesXaxis(dates) {
  const manyPoints = dates.length > 7
  return {
    categories: dates,
    tickAmount: manyPoints ? 6 : dates.length,
    labels: {
      rotate: manyPoints ? -25 : 0,
      rotateAlways: false,
      hideOverlappingLabels: true,
      trim: true,
      maxHeight: 48,
      style: { colors: CHART_UI.label, fontSize: '10px', fontWeight: 500 },
      formatter: formatDateTick,
    },
    tooltip: { enabled: false },
  }
}

export function buildViewsTimeSeries(data) {
  if (!data?.dates?.length) return null

  return {
    series: [{ name: 'Views', data: data.views ?? [] }],
    options: createBaseChartOptions({
      chart: {
        type: 'area',
        dropShadow: {
          enabled: true,
          color: CHART_COLORS.brand,
          top: 6,
          blur: 16,
          opacity: 0.2,
        },
      },
      colors: [CHART_COLORS.brand],
      stroke: chartStrokeGlow(CHART_COLORS.brand),
      fill: chartGradientFill(CHART_COLORS.brand, 0.5, 0.01),
      markers: {
        size: 0,
        strokeWidth: 0,
        hover: { size: 6, sizeOffset: 2 },
      },
      xaxis: timeSeriesXaxis(data.dates),
      yaxis: {
        labels: { formatter: (v) => formatCompactNumber(v) },
        tickAmount: 5,
      },
      tooltip: enhancedTooltip((v) => v.toLocaleString()),
      legend: { show: false },
    }),
  }
}

export function buildEngagementTimeSeries(data) {
  if (!data?.dates?.length) return null

  const values = data.views ?? data.engagements ?? []

  return {
    series: [{ name: 'Engagement rate', data: values }],
    options: createBaseChartOptions({
      chart: {
        type: 'area',
        dropShadow: {
          enabled: true,
          color: CHART_COLORS.purple,
          top: 6,
          blur: 16,
          opacity: 0.18,
        },
      },
      colors: [CHART_COLORS.purple],
      stroke: chartStrokeGlow(CHART_COLORS.purple),
      fill: chartGradientFill(CHART_COLORS.purple, 0.4, 0.01),
      markers: {
        size: 4,
        strokeColors: '#0A0A0A',
        strokeWidth: 2,
        fillOpacity: 1,
        hover: { size: 7, sizeOffset: 2 },
      },
      xaxis: timeSeriesXaxis(data.dates),
      yaxis: {
        min: 0,
        max: 1,
        tickAmount: 5,
        labels: { formatter: (v) => `${Math.round(v * 100)}%` },
      },
      tooltip: enhancedTooltip((v) => `${(v * 100).toFixed(1)}%`),
      legend: { show: false },
    }),
  }
}

function resolveBucketViews(item) {
  return item.avg_views ?? item.avg_reach ?? 0
}

const dualBarPlotOptions = {
  bar: {
    horizontal: false,
    columnWidth: '48%',
    borderRadius: 8,
    borderRadiusApplication: 'end',
    borderRadiusWhenStacked: 'last',
    dataLabels: { position: 'top' },
  },
}

const singleBarPlotOptions = {
  bar: {
    distributed: true,
    horizontal: false,
    columnWidth: '42%',
    borderRadius: 10,
    borderRadiusApplication: 'end',
  },
}

function bucketLegend() {
  return {
    ...enhancedLegend(),
    position: 'bottom',
    horizontalAlign: 'center',
    offsetY: 4,
    fontSize: '11px',
    itemMargin: { horizontal: 8, vertical: 4 },
  }
}

function dualYaxisConfig() {
  return [
    {
      title: { show: false },
      labels: {
        formatter: (v) => formatCompactNumber(v),
        style: { fontSize: '10px' },
      },
      tickAmount: 4,
    },
    {
      opposite: true,
      min: 0,
      max: 1,
      tickAmount: 5,
      title: { show: false },
      labels: {
        formatter: (v) => `${Math.round(v * 100)}%`,
        style: { fontSize: '10px' },
      },
    },
  ]
}

export function buildDualMetricBucketChart(items, labelKey) {
  if (!items?.length) return null

  const categories = items.map((item) => formatLabel(item[labelKey]))

  return {
    series: [
      { name: 'Avg views', data: items.map(resolveBucketViews) },
      { name: 'Avg engagement', data: items.map((item) => item.avg_engagement ?? 0) },
    ],
    options: createBaseChartOptions({
      chart: {
        type: 'bar',
        dropShadow: { enabled: false },
      },
      colors: [CHART_COLORS.brand, CHART_COLORS.amber],
      plotOptions: dualBarPlotOptions,
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          type: 'vertical',
          shadeIntensity: 0.25,
          opacityFrom: 0.95,
          opacityTo: 0.65,
          stops: [0, 100],
        },
      },
      xaxis: {
        categories,
        labels: {
          trim: true,
          hideOverlappingLabels: true,
          maxHeight: 56,
          style: { colors: CHART_UI.label, fontSize: '10px', fontWeight: 500 },
        },
      },
      yaxis: dualYaxisConfig(),
      legend: bucketLegend(),
      tooltip: {
        ...enhancedTooltip(),
        y: [
          { formatter: (v) => v.toLocaleString() },
          { formatter: (v) => `${(v * 100).toFixed(1)}%` },
        ],
      },
    }),
  }
}

export function buildEngagementBucketChart(items, labelKey) {
  if (!items?.length) return null

  const categories = items.map((item) => formatLabel(item[labelKey]))

  return {
    series: [{ name: 'Avg engagement', data: items.map((item) => item.avg_engagement ?? 0) }],
    options: createBaseChartOptions({
      chart: { type: 'bar', dropShadow: { enabled: false } },
      colors: CHART_COLOR_SEQUENCE,
      plotOptions: singleBarPlotOptions,
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          type: 'vertical',
          shadeIntensity: 0.3,
          opacityFrom: 0.9,
          opacityTo: 0.55,
          stops: [0, 100],
        },
      },
      xaxis: {
        categories,
        labels: {
          style: { colors: CHART_UI.label, fontSize: '11px', fontWeight: 500 },
        },
      },
      yaxis: {
        min: 0,
        max: 1,
        tickAmount: 5,
        labels: { formatter: (v) => `${Math.round(v * 100)}%` },
      },
      legend: { show: false },
      tooltip: enhancedTooltip((v) => `${(v * 100).toFixed(1)}%`),
    }),
  }
}

export function buildContentTypeBucketChart(data) {
  return buildDualMetricBucketChart(data?.by_content_type, 'type')
}

export function buildTimeBucketChart(data) {
  return buildDualMetricBucketChart(data?.by_time, 'time')
}

export function buildDurationBucketChart(data) {
  return buildEngagementBucketChart(data?.by_duration, 'range')
}
