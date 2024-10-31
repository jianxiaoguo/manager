import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// https://vitejs.dev/config/

const USE_PROXY = true
const MANAGER_SERVICE_URL = process.env.MANAGER_SERVICE_URL ? process.env.MANAGER_SERVICE_URL : '/v1'

export default defineConfig(async ({ command, mode }) => {
  return {
    css: {
      postcss: {
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
    server: {
      proxy: { // 代理配置
        '/v1': {
          target: MANAGER_SERVICE_URL,
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
        VUE_APP_SERVICE_URL: USE_PROXY ? '/v1' : MANAGER_SERVICE_URL,
      },
      __VUE_I18N_FULL_INSTALL__: true,
      __VUE_I18N_LEGACY_API__: false,
      __INTLIFY_PROD_DEVTOOLS__: false,
    }
  }
})
