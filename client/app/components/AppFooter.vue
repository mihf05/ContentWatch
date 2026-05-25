<template>
  <footer
    class="w-full border-t border-white/5 bg-jetblack pt-12 sm:pt-16 pb-6 px-4 sm:px-6 md:px-12 mt-auto z-10 relative">
    <div
      class="max-w-screen-2xl mx-auto w-full grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8 sm:gap-10 lg:gap-8 mb-12 sm:mb-16">

      <!-- Brand & Description -->
      <div class="col-span-2 sm:col-span-2 md:col-span-3 lg:col-span-2 flex flex-col gap-4 sm:gap-6">
        <AppLogo />
        <p class="font-body-sm text-body-sm text-gray-400 max-w-sm">
          AI-Driven Creator Intelligence. Stop guessing what works and start growing your audience with data-backed
          content strategies.
        </p>
      </div>

      <!-- Links: Platform -->
      <div class="flex flex-col gap-3 sm:gap-4">
        <h4 class="font-label-md text-label-md text-brand uppercase tracking-wider mb-1 sm:mb-2">Platform</h4>
        <NuxtLink to="/#solutions"
          class="font-body-sm text-body-sm text-gray-400 hover:text-brand transition-colors">Solutions</NuxtLink>
        <NuxtLink to="/#analytics"
          class="font-body-sm text-body-sm text-gray-400 hover:text-brand transition-colors">Analytics</NuxtLink>
        <NuxtLink to="/#features"
          class="font-body-sm text-body-sm text-gray-400 hover:text-brand transition-colors">Features</NuxtLink>
      </div>

      <!-- Links: Account -->
      <div class="flex flex-col gap-3 sm:gap-4">
        <h4 class="font-label-md text-label-md text-brand uppercase tracking-wider mb-1 sm:mb-2">Account</h4>
        <NuxtLink to="/login" class="font-body-sm text-body-sm text-gray-400 hover:text-brand transition-colors">Sign In
        </NuxtLink>
        <NuxtLink to="/register" class="font-body-sm text-body-sm text-gray-400 hover:text-brand transition-colors">Sign
          Up</NuxtLink>
      </div>

      <!-- Links: Company -->
      <div class="flex flex-col gap-3 sm:gap-4 col-span-2 sm:col-span-1">
        <h4 class="font-label-md text-label-md text-brand uppercase tracking-wider mb-1 sm:mb-2">Company</h4>
        <NuxtLink to="/about" class="font-body-sm text-body-sm text-gray-400 hover:text-brand transition-colors">About
        </NuxtLink>
      </div>

    </div>

    <div
      class="max-w-screen-2xl mx-auto w-full pt-5 sm:pt-6 border-t border-white/10 flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4">
      <div class="font-body-sm text-[12px] sm:text-[13px] text-gray-500">
        © {{ new Date().getFullYear() }} ContentWatch Intelligence. All rights reserved.
      </div>
    </div>
  </footer>
</template>
