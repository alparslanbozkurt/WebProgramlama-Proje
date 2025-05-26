import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // frontend konteynerindeki `/api` isteklerini backend konteynerine yönlendir
      '/api': {
        // Docker Compose'da service adı muhtemelen "backend"
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
