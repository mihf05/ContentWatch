<script setup>
defineProps({
  size: {
    type: String,
    default: 'md'
  },
  collapsed: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <NuxtLink to="/" class="flex items-center gap-2 group outline-none">
    <div
      class="relative flex items-center justify-center rounded-lg bg-linear-to-br from-brand/20 to-brand/5 border border-brand/20 group-hover:border-brand/40 transition-colors"
      :class="[
        size === 'sm' ? 'w-6 h-6' : size === 'lg' ? 'w-10 h-10' : 'w-8 h-8'
      ]">
      <Icon name="material-symbols:radar" class="text-brand" :class="[
        size === 'sm' ? 'text-sm' : size === 'lg' ? 'text-2xl' : 'text-xl'
      ]" />
    </div>
    <div v-if="!collapsed" class="font-bold tracking-tight flex items-center" :class="[
      size === 'sm' ? 'text-lg' : size === 'lg' ? 'text-3xl' : 'text-2xl text-headline-md font-headline-md'
    ]">
      <span class="text-white">Content</span><span class="text-brand">Watch</span>
    </div>
  </NuxtLink>
</template>
