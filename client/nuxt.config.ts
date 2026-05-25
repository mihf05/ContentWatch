// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  debug: false,

  app: {
    head: {
      title: 'ContentWatch - AI-Driven Creator Intelligence',
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
		public: {
			apiBase: import.meta.env.API_URL,
		}
	},
})
