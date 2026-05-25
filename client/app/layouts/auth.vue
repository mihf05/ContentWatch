<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden px-6 py-12"
    style="background: radial-gradient(ellipse 80% 60% at 10% 20%, rgba(77, 220, 198, 0.12) 0%, transparent 60%), radial-gradient(ellipse 60% 50% at 90% 80%, rgba(77, 220, 198, 0.08) 0%, transparent 55%), radial-gradient(ellipse 40% 40% at 50% 50%, rgba(77, 220, 198, 0.05) 0%, transparent 50%), #0A0A0A;">

    <!-- Subtle grid overlay -->
    <div class="absolute inset-0 opacity-[0.03] pointer-events-none"
      style="background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 60px 60px;">
    </div>

    <div class="relative z-10 w-full max-w-md">
      <slot />
    </div>
  </div>
</template>
