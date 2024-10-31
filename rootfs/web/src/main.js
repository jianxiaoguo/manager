import App from './App.vue'
import router from './router'
import { createApp } from 'vue'
import store from './store'
import VueApexCharts from "vue3-apexcharts";
import { i18n, setLang, getUAgentLang, getLang } from './lang'
import {install} from '@icon-park/vue-next/es/all';
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import moment from 'moment/src/moment'
import { dinero, toDecimal} from 'dinero.js';


/**
 * 时间对象的格式化;
 */
Date.prototype.format = function(format) {
    /*
     * eg:format="yyyy-MM-dd hh:mm:ss";
     */
    return moment(this).format(format)
}

// 初始化
function init () {
    // 语言初始化
    const lang = getUAgentLang()
    setLang(lang.replace("_", "-"))
}

init()

router.store = store //Inject store
const app = createApp(App)

app.config.globalProperties.$toPrice = function(amount, factor=5) {
    const currency = {
        code: 'EUR',
        base: 10,
        exponent: factor,
    };
    var d = dinero({ amount: amount, currency: currency})
    return toDecimal(d, function({ amount, currency }) {
        return amount.toLocaleString(getLang(), {
            maximumSignificantDigits: factor,
            style: 'currency',
            currency: currency.code,
        });
    })
}

install(app);
app.use(store)
app.use(i18n)
app.use(VueApexCharts)
app.use(ElementPlus)
app.use(router)
app.mount('#app')