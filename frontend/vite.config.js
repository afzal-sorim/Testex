import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    watch: {
      ignored: ['**/playwright-report/**', '**/test-results/**'],
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        ws: true,
        timeout: 300000,
        proxyTimeout: 300000,
      }
    },
  },
})
