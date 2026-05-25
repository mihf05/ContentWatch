<script setup>
const authStore = useAuthStore()

if (!authStore.user) {
  await authStore.fetchUser()
}

const developers = [
  {
    name: 'S.M Nazmus Sadat',
    role: 'Leader, Backend Dev',
    bio: '',
    avatar: 'https://avatars.githubusercontent.com/u/214529054',
    github: 'https://github.com/smsadat1',
    linkedin: 'https://www.linkedin.com/in/sm-sadat-461755369/'
  },
  {
    name: 'Atia Farha',
    role: 'Frontend Dev',
    bio: '',
    avatar: 'https://avatars.githubusercontent.com/u/119663174',
    github: 'https://github.com/Atia-Farha',
    linkedin: 'https://www.linkedin.com/in/atia-farha/'
  },
  {
    name: 'Md Irfan Hasan Fahim',
    role: 'Backend Dev',
    bio: '',
    avatar: 'https://avatars.githubusercontent.com/u/81842071',
    github: 'https://github.com/mihf05',
    linkedin: 'https://www.linkedin.com/in/mihf05/'
  },
]
</script>

<template>
  <main class="relative min-h-screen pt-24 pb-16 px-4 sm:px-6 md:px-12 max-w-screen-xl mx-auto w-full overflow-hidden">
    <!-- Glow effect behind hero -->
    <div class="hero-glow"></div>

    <!-- About Hero Section -->
    <div class="relative z-10 text-center max-w-3xl mx-auto mt-8 md:mt-12 mb-16 md:mb-24">
      <div
        class="inline-block px-4 py-2 border border-brand/20 rounded-full bg-brand/10 mb-6 font-label-md text-label-md text-brand uppercase tracking-wider">
        Our Mission
      </div>
      <h1 class="font-display-lg text-display-lg text-white mb-6">
        Empowering Creators with <span class="text-brand">Actionable Intelligence</span>
      </h1>
      <p class="font-body-lg text-body-lg text-gray-400">
        At ContentWatch, we believe every creator deserves clear, data-driven insights. Our platform cuts through the
        noise of raw metrics to deliver beautiful, strategic suggestions that grow your audience and build your
        business.
      </p>
    </div>

    <!-- Developer Grid -->
    <div class="relative z-10">
      <h2 class="font-headline-lg text-headline-lg text-brand text-center mb-4">Meet the Visionaries</h2>
      <p class="font-body-md text-body-md text-gray-400 text-center max-w-lg mx-auto mb-12 sm:mb-16">
        The team dedicated to building the future of AI-driven analytical tools for digital creators worldwide.
      </p>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <!-- Developer Profile Card -->
        <div v-for="dev in developers" :key="dev.name"
          class="glass-card rounded-2xl p-6 flex flex-col items-center text-center transition-all duration-300 hover:-translate-y-2 hover:border-brand/40 group">

          <div class="relative mb-6">
            <!-- Glow around avatar on hover -->
            <div
              class="absolute inset-0 rounded-full bg-brand/20 blur-md opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            </div>
            <img :src="dev.avatar" :alt="dev.name"
              class="w-24 h-24 rounded-full object-cover border-2 border-white/10 group-hover:border-brand transition-colors duration-300 relative z-10" />
          </div>

          <h3
            class="font-headline-md text-headline-md text-white group-hover:text-brand transition-colors duration-200">
            {{ dev.name }}</h3>
          <span class="font-label-md text-label-md text-gray-400 font-medium mb-4 block">{{ dev.role }}</span>

          <p class="font-body-sm text-body-sm text-gray-400 mb-6 flex-grow">
            {{ dev.bio }}
          </p>

          <div class="flex gap-4 mt-auto">
            <a :href="dev.github" class="text-gray-400 hover:text-white transition-colors" aria-label="GitHub"
              target="_blank">
              <Icon name="mdi:github" class="text-xl" />
            </a>
            <a :href="dev.linkedin" class="text-gray-400 hover:text-white transition-colors" aria-label="LinkedIn"
              target="_blank">
              <Icon name="mdi:linkedin" class="text-xl" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
