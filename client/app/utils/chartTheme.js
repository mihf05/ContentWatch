export const CHART_COLORS = {
  brand: '#4DDCC6',
  purple: '#7C6FFF',
  amber: '#F59E0B',
  orange: '#F97316',
  muted: '#6B7280',
}

export const CHART_COLOR_SEQUENCE = [
  CHART_COLORS.brand,
  CHART_COLORS.purple,
  CHART_COLORS.amber,
  CHART_COLORS.orange,
  CHART_COLORS.muted,
]

export const CHART_UI = {
  grid: 'rgba(255, 255, 255, 0.05)',
  gridHighlight: 'rgba(77, 220, 198, 0.08)',
  axis: '#6B7280',
  label: '#9CA3AF',
  legend: '#D1D5DB',
  tooltipBg: '#141414',
  tooltipBorder: 'rgba(77, 220, 198, 0.18)',
  crosshair: 'rgba(77, 220, 198, 0.35)',
}

/** Apex gradient fill from a hex color (area / bar). */
export function chartGradientFill(color, opacityFrom = 0.45, opacityTo = 0.02) {
  return {
    type: 'gradient',
    gradient: {
      shade: 'dark',
      type: 'vertical',
      shadeIntensity: 0.4,
      opacityFrom,
      opacityTo,
      stops: [0, 55, 100],
      colorStops: [
        { offset: 0, color, opacity: opacityFrom },
        { offset: 55, color, opacity: opacityFrom * 0.35 },
        { offset: 100, color, opacity: opacityTo },
      ],
    },
  }
}

export function chartStrokeGlow(color) {
  return {
    curve: 'smooth',
    width: 3,
    lineCap: 'round',
    colors: [color],
  }
}
