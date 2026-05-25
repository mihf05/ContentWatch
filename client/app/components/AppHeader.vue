<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const navLinks = [
  { name: 'Solutions', href: '#solutions' },
  { name: 'Analytics', href: '#analytics' },
  { name: 'Features', href: '#features' }
]
</script>

<template>
  <header class="fixed top-0 w-full z-50 transition-all duration-300 bg-jetblack/80 backdrop-blur-md border-b border-white/10">
    <nav class="flex justify-between items-center px-4 sm:px-6 md:px-12 py-3 sm:py-4 max-w-screen-2xl mx-auto w-full">
      <AppLogo />

      <!-- Desktop Nav -->
      <div class="hidden md:flex gap-8 items-center">
        <a v-for="link in navLinks" :key="link.name" :href="link.href"
          class="font-label-md text-label-md text-gray-400 font-medium hover:text-brand transition-colors duration-200">
          {{ link.name }}
        </a>
      </div>
      
      <!-- Desktop Actions -->
      <div class="hidden md:flex items-center gap-4">
        <NuxtLink to="/login"
          class="font-label-md text-label-md text-gray-400 hover:text-brand transition-colors">Login</NuxtLink>
        <NuxtLink to="/register"
          class="bg-brand text-jetblack font-label-md text-label-md px-6 py-2 rounded-full hover:shadow-[0_0_15px_rgba(77,220,198,0.4)] transition-shadow font-bold">Get Started</NuxtLink>
      </div>

      <!-- Mobile Menu Button -->
      <button class="md:hidden flex items-center text-white hover:text-brand transition-colors" @click="toggleMenu"
        aria-label="Toggle Menu">
        <Icon :name="isMenuOpen ? 'material-symbols:close-rounded' : 'material-symbols:menu-rounded'"
          class="text-2xl sm:text-3xl" />
      </button>
    </nav>

    <!-- Mobile Nav -->
    <div v-show="isMenuOpen"
      class="md:hidden absolute top-full left-0 w-full bg-neutral-900 border-b border-white/10 flex flex-col items-center py-5 sm:py-6 gap-4 sm:gap-6 shadow-2xl">
      <a v-for="link in navLinks" :key="link.name" :href="link.href" @click="isMenuOpen = false"
        class="text-[16px] sm:text-[18px] text-white hover:text-brand transition-colors duration-200 w-full text-center py-1.5 sm:py-2 font-medium">
        {{ link.name }}
      </a>

      <div class="w-full px-6 sm:px-8 mt-1 sm:mt-2 flex flex-col gap-3 sm:gap-4">
        <NuxtLink to="/login" @click="isMenuOpen = false"
          class="block w-full py-2.5 sm:py-3 border border-white/10 rounded-full font-label-md text-label-md text-white hover:bg-white/5 transition-colors text-center">
          Login</NuxtLink>
        <NuxtLink to="/register" @click="isMenuOpen = false"
          class="block w-full bg-brand text-jetblack font-bold font-label-md text-label-md py-2.5 sm:py-3 rounded-full hover:shadow-[0_0_15px_rgba(77,220,198,0.4)] transition-shadow text-center">
          Get Started</NuxtLink>
      </div>
    </div>
  </header>
</template>
