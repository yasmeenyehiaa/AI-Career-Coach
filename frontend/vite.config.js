import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    // In development, forward every /api request to the FastAPI backend.
    // This way the frontend can call "/api/..." exactly like in production.
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
