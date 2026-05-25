<script setup>
definePageMeta({ layout: 'auth', middleware: 'guest' })

useHead({ title: 'Sign Up' })

const authStore = useAuthStore()
const { showPopup } = usePopup()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

async function handleRegister() {
  if (!email.value || !password.value || !confirmPassword.value) {
    showPopup('Please fill in all fields', 'error')
    return
  }

  if (password.value !== confirmPassword.value) {
    showPopup('Passwords do not match', 'error')
    return
  }

  if (password.value.length < 8) {
    showPopup('Password must be at least 8 characters long', 'error')
    return
  }

  const success = await authStore.register(email.value, password.value, confirmPassword.value)
  if (success) {
    navigateTo('/dashboard')
  }
}
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
        <h1 class="text-2xl font-bold text-brand mb-2">Create your account</h1>
        <p class="text-gray-400 text-sm">Start growing with data-backed strategies</p>
      </div>

      <form @submit.prevent="handleRegister" class="flex flex-col gap-5">
        <!-- Email -->
        <div class="flex flex-col gap-2">
          <label for="register-email" class="text-sm font-medium text-gray-300">Email</label>
          <div class="relative">
            <Icon name="material-symbols:mail-outline"
              class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 text-lg" />
            <input id="register-email" v-model="email" type="email" placeholder="you@example.com" autocomplete="email"
              :disabled="authStore.isLoading"
              class="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-11 pr-4 text-white placeholder-gray-500 text-sm outline-none focus:border-brand/50 focus:ring-1 focus:ring-brand/30 transition-all disabled:opacity-50" />
          </div>
        </div>

        <!-- Password -->
        <div class="flex flex-col gap-2">
          <label for="register-password" class="text-sm font-medium text-gray-300">Password</label>
          <div class="relative">
            <Icon name="material-symbols:lock-outline"
              class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 text-lg" />
            <input id="register-password" v-model="password" :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••" autocomplete="new-password" :disabled="authStore.isLoading"
              class="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-11 pr-11 text-white placeholder-gray-500 text-sm outline-none focus:border-brand/50 focus:ring-1 focus:ring-brand/30 transition-all disabled:opacity-50" />
            <button type="button" @click="showPassword = !showPassword"
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors">
              <Icon
                :name="showPassword ? 'material-symbols:visibility-off-outline' : 'material-symbols:visibility-outline'"
                class="text-lg" />
            </button>
          </div>
        </div>

        <!-- Confirm Password -->
        <div class="flex flex-col gap-2">
          <label for="register-confirm" class="text-sm font-medium text-gray-300">Confirm Password</label>
          <div class="relative">
            <Icon name="material-symbols:lock-outline"
              class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 text-lg" />
            <input id="register-confirm" v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="••••••••" autocomplete="new-password" :disabled="authStore.isLoading"
              class="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-11 pr-11 text-white placeholder-gray-500 text-sm outline-none focus:border-brand/50 focus:ring-1 focus:ring-brand/30 transition-all disabled:opacity-50" />
            <button type="button" @click="showConfirmPassword = !showConfirmPassword"
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors">
              <Icon
                :name="showConfirmPassword ? 'material-symbols:visibility-off-outline' : 'material-symbols:visibility-outline'"
                class="text-lg" />
            </button>
          </div>
        </div>

        <!-- Submit -->
        <button type="submit" :disabled="authStore.isLoading"
          class="w-full bg-brand text-jetblack font-bold text-sm py-3 rounded-xl hover:shadow-[0_0_20px_rgba(77,220,198,0.35)] transition-all mt-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
          <span v-if="authStore.isLoading"
            class="inline-block animate-spin rounded-full h-4 w-4 border-2 border-current border-t-transparent"
            role="status"></span>
          {{ authStore.isLoading ? 'Creating Account...' : 'Create Account' }}
        </button>
      </form>

      <!-- Divider -->
      <div class="flex items-center gap-4 my-6">
        <div class="h-px grow bg-white/10"></div>
      </div>

      <p class="text-center text-sm text-gray-500 mt-8">
        Already have an account? <NuxtLink to="/login"
          class="text-brand hover:text-brand/80 font-medium transition-colors">Sign In</NuxtLink>
      </p>
    </div>
  </div>
</template>
