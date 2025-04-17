import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueApexCharts from 'vue3-apexcharts'
import { i18n, setLang, getUAgentLang, getLang } from './lang'
import { install } from '@icon-park/vue-next/es/all'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/element-plus/index.css'
import moment from 'moment/src/moment'
import { dinero, toDecimal } from 'dinero.js'

// 时间对象的格式化
function formatDate(date, format) {
  return moment(date).format(format)
}

// 初始化
function init() {
  // 语言初始化
  const lang = getUAgentLang()
  setLang(lang.replace('_', '-'))
}

init()

router.store = store // Inject store
const app = createApp(App)

app.config.globalProperties.$formatDate = formatDate

app.config.globalProperties.$toPrice = function(amount, factor = 5) {
  const currency = {
    code: 'EUR',
    base: 10,
    exponent: factor,
  }
  const d = dinero({ amount, currency })
  return toDecimal(d, ({ amount, currency }) => {
    amount = amount || 0
    return amount.toLocaleString(getLang(), {
      maximumSignificantDigits: factor,
      style: 'currency',
      currency: currency.code,
    })
  })
}

install(app)
app.use(store)
app.use(i18n)
app.use(VueApexCharts)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
