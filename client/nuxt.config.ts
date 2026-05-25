// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  debug: false,

  app: {
    head: {
      link: [
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap' }
      ]
    }
  },

  css: ['@/assets/css/main.css'],

  modules: [
    '@vueuse/nuxt',
    '@nuxt/icon',
    '@nuxt/image',
    '@pinia/nuxt',
  ],

  vite: {
    plugins: [tailwindcss()],
  },

  runtimeConfig: {
    // Server-only — used by SSR $fetch so it hits Django directly
    apiBaseServer: 'http://127.0.0.1:8000/api',
    public: {
      apiBase: '/api',
    }
  },

  // Proxy /api requests to Django backend — avoids CORS in development
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/api',
        changeOrigin: true,
      },
    },
  },
})
