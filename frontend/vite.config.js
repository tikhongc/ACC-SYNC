import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // 允许外部访问
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080', // 明确使用IPv4地址
        changeOrigin: true,
        secure: false,
        timeout: 10000,
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            console.log('Sending Request to the Target:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
          });
        }
      },
      '/health': {
        target: 'http://127.0.0.1:8080', // 明确使用IPv4地址
        changeOrigin: true,
        secure: false,
        timeout: 10000
      },
      '/auth': {
        target: 'http://127.0.0.1:8080', // 代理认证相关路由到Flask
        changeOrigin: true,
        secure: false,
        timeout: 10000
      }
    }
  },
  build: {
    outDir: '../static/dist',
    assetsDir: 'assets',
    emptyOutDir: true
  }
})
