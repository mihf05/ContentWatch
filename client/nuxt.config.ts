// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  debug: false,

  css: ['@/assets/css/main.css'],

  modules: [
    '@vueuse/nuxt',
    '@nuxt/icon',
    // '@nuxt/image',
    // '@pinia/nuxt',
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
