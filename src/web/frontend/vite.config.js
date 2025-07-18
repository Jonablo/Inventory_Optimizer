import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 3000,
    proxy: {
      "/api": {
        "target": "http://0.0.0.0:5000",
        "changeOrigin": true,
        "rewrite": (p) => p.replace(/^\/api/, "")
      }
    }
  }
});