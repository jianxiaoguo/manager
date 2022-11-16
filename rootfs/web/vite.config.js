import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// https://vitejs.dev/config/

VUE_APP_BASE_URL = process.env.VUE_APP_BASE_URL ? process.env.VUE_APP_BASE_URL : '/v1'
export default defineConfig({
  css: {
    postcss:{
      plugins: [
        {
            postcssPlugin: 'internal:charset-removal',
            AtRule: {
                charset: (atRule) => {
                    if (atRule.name === 'charset') {
                        atRule.remove()
                    }
                }
            }
        }
      ]
    }
  },
  server:{
    proxy: { // 代理配置
      '/v1/avatar': {
        target: VUE_APP_BASE_URL,
        rewrite: path => path.replace(/^\/v1/, ''),
        changeOrigin: true,
      }
    },
  },
  plugins: [vue()],
  build: {
    minify: true,
    chunkSizeWarningLimit: 5000,
    rollupOptions: {
      output: {
          manualChunks: {
              'vue': ['vue', 'vue-router', 'vuex'],
              'element-plus': ['element-plus'],
              'apexcharts': ['apexcharts'],
          }
      }
    }
  },
  define: {
    'process.env': {
      VUE_APP_BASE_URL: VUE_APP_BASE_URL,
    },
    __VUE_I18N_FULL_INSTALL__: true,
    __VUE_I18N_LEGACY_API__: false,
    __INTLIFY_PROD_DEVTOOLS__: false,
  }
})
