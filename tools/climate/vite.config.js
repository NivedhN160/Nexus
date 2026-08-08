import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://terrax1-gfp5u3xc.b4a.run',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})

