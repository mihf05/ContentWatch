<script setup>
import { ref } from 'vue'

definePageMeta({ layout: 'auth' })

useHead({ title: 'Login — ContentWatch' })

const email = ref('')
const password = ref('')
const showPassword = ref(false)
</script>

<template>
  <div>
    <!-- Logo -->
    <div class="flex justify-center mb-10">
      <AppLogo size="lg" />
    </div>

    <!-- Card -->
    <div class="glass-card rounded-2xl p-8 md:p-10">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-brand mb-2">Welcome back</h1>
        <p class="text-gray-400 text-sm">Sign in to your account to continue</p>
      </div>

      <form @submit.prevent class="flex flex-col gap-5">
        <!-- Email -->
        <div class="flex flex-col gap-2">
          <label for="login-email" class="text-sm font-medium text-gray-300">Email</label>
          <div class="relative">
            <Icon name="material-symbols:mail-outline"
              class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 text-lg" />
            <input id="login-email" v-model="email" type="email" placeholder="you@example.com" autocomplete="email"
              class="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-11 pr-4 text-white placeholder-gray-500 text-sm outline-none focus:border-brand/50 focus:ring-1 focus:ring-brand/30 transition-all" />
          </div>
        </div>

        <!-- Password -->
        <div class="flex flex-col gap-2">
          <div class="flex items-center justify-between">
            <label for="login-password" class="text-sm font-medium text-gray-300">Password</label>
            <NuxtLink to="#" class="text-xs text-brand hover:text-brand/80 transition-colors">Forgot password?
            </NuxtLink>
          </div>
          <div class="relative">
            <Icon name="material-symbols:lock-outline"
              class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 text-lg" />
            <input id="login-password" v-model="password" :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••" autocomplete="current-password"
              class="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-11 pr-11 text-white placeholder-gray-500 text-sm outline-none focus:border-brand/50 focus:ring-1 focus:ring-brand/30 transition-all" />
            <button type="button" @click="showPassword = !showPassword"
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors">
              <Icon
                :name="showPassword ? 'material-symbols:visibility-off-outline' : 'material-symbols:visibility-outline'"
                class="text-lg" />
            </button>
          </div>
        </div>

        <!-- Submit -->
        <button type="submit"
          class="w-full bg-brand text-jetblack font-bold text-sm py-3 rounded-xl hover:shadow-[0_0_20px_rgba(77,220,198,0.35)] transition-all mt-2">
          Sign In
        </button>
      </form>

      <!-- Divider -->
      <div class="flex items-center gap-4 my-6">
        <div class="h-px flex-grow bg-white/10"></div>
      </div>

      <p class="text-center text-sm text-gray-500 mt-8">
        Don't have an account? <NuxtLink to="/register"
          class="text-brand hover:text-brand/80 font-medium transition-colors">Sign Up</NuxtLink>
      </p>
    </div>
  </div>
</template>
