<script setup>
const authStore = useAuthStore()
const route = useRoute()

if (!authStore.user) {
  await authStore.fetchUser()
}

const isSidebarOpen = ref(false)
const isCollapsed = ref(false)

onMounted(() => {
  isCollapsed.value = localStorage.getItem('cw_sidebar_collapsed') === 'true'
})

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
  localStorage.setItem('cw_sidebar_collapsed', isCollapsed.value)
}

const navItems = [
  { label: 'Overview', icon: 'dashboard', to: '/dashboard' },
  { label: 'Content DNA', icon: 'genetics', to: '/dashboard/content-dna' },
  { label: 'Analytics', icon: 'analytics', to: '/dashboard/analytics' },
  { label: 'Integrations', icon: 'extension', to: '/dashboard/integrations' },
  { label: 'Settings', icon: 'settings', to: '/dashboard/settings' },
]

function handleLogout() {
  authStore.logout()
}

function closeSidebar() {
  isSidebarOpen.value = false
}

const userInitial = computed(() => {
  return authStore.user?.email?.charAt(0)?.toUpperCase() || 'U'
})
</script>

<template>
  <div class="min-h-screen flex bg-jetblack">

    <!-- Mobile overlay -->
    <Transition name="fade">
      <div v-if="isSidebarOpen" class="fixed inset-0 z-40 bg-black/60 md:hidden" @click="closeSidebar" />
    </Transition>

    <!-- Sidebar -->
    <aside
      class="fixed md:sticky top-0 left-0 z-50 h-screen flex flex-col bg-[#111111] border-r border-white/[0.06] transition-all duration-300"
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
        isCollapsed ? 'md:w-[72px]' : 'md:w-[260px]'
      ]">
      <!-- Logo -->
      <div class="h-16 flex items-center justify-between px-5 border-b border-white/[0.06]">
        <AppLogo size="sm" :collapsed="isCollapsed" />
        <button @click="toggleSidebar"
          class="hidden md:flex items-center justify-center text-gray-400 hover:text-white transition-colors cursor-pointer">
          <span class="material-symbols-outlined text-xl">{{ isCollapsed ? 'chevron_right' : 'chevron_left' }}</span>
        </button>
      </div>

      <!-- Nav Items -->
      <nav class="flex-1 px-3 py-4 flex flex-col gap-1 overflow-y-auto" :class="isCollapsed ? 'items-center' : ''">
        <NuxtLink v-for="item in navItems" :key="item.to" :to="item.to" @click="closeSidebar"
          class="flex items-center gap-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 group"
          :class="[
            route.path === item.to
              ? 'bg-brand/10 text-brand'
              : 'text-gray-400 hover:text-white hover:bg-white/[0.04]',
            isCollapsed ? 'px-0 justify-center w-10 h-10' : 'px-3 w-full'
          ]">
          <span class="material-symbols-outlined text-xl flex-shrink-0">{{ item.icon }}</span>
          <span v-if="!isCollapsed" class="whitespace-nowrap">{{ item.label }}</span>
        </NuxtLink>
      </nav>

      <!-- User section -->
      <div class="px-3 pb-4 border-t border-white/[0.06] pt-3">
        <div class="flex items-center gap-3 py-2" :class="isCollapsed ? 'justify-center' : 'px-3'">
          <div
            class="w-8 h-8 rounded-full bg-brand/15 border border-brand/30 flex items-center justify-center text-brand text-xs font-bold flex-shrink-0">
            {{ userInitial }}
          </div>
          <div v-if="!isCollapsed" class="flex-1 min-w-0">
            <p class="text-xs text-white font-medium truncate">{{ authStore.user?.email }}</p>
          </div>
        </div>
        <button @click="handleLogout"
          class="w-full mt-2 flex items-center gap-3 py-2.5 rounded-xl text-sm text-gray-400 hover:text-red-400 hover:bg-red-500/5 transition-all duration-200 cursor-pointer"
          :class="isCollapsed ? 'px-0 justify-center w-10 h-10 mx-auto' : 'px-3'">
          <span class="material-symbols-outlined text-xl flex-shrink-0">logout</span>
          <span v-if="!isCollapsed">Log out</span>
        </button>
      </div>
    </aside>

    <!-- Main content area -->
    <div class="flex-1 flex flex-col min-w-0">

      <!-- Top bar -->
      <header
        class="sticky top-0 z-30 h-16 flex items-center justify-between px-4 md:px-8 bg-jetblack/80 backdrop-blur-md border-b border-white/[0.06]">
        <!-- Mobile menu toggle -->
        <button @click="isSidebarOpen = true"
          class="md:hidden text-gray-400 hover:text-white transition-colors -ml-1 cursor-pointer">
          <span class="material-symbols-outlined text-2xl">menu</span>
        </button>

        <!-- Page title -->
        <h1 class="text-white text-base font-semibold hidden md:block">
          {{navItems.find(i => i.to === route.path)?.label || 'Dashboard'}}
        </h1>
      </header>

      <!-- Page content slot -->
      <main class="flex-1 min-w-0 px-4 md:px-8 py-6 md:py-8 overflow-x-hidden overflow-y-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
