import {onMounted, reactive, toRefs} from "vue";
import { getInvoices } from '../services/bill'

export default {
    name: "AccountInvoices",
    setup() {
        const state = reactive({
            moreInvoices:[],
            lessInvoices:[],
            showMore: false,
            lessShowLine: 6,
        })

        const getFormattedDate = (period) => {
            var date = new Date(period * 1000)
            var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            return `${months[date.getMonth()]} ${date.getFullYear()}`
        }

        const showMoreInvoices = async () => {
            state.showMore = !state.showMore;
        }

        onMounted(async () => { 
            let res = await getInvoices(300, 0)
            state.moreInvoices = res.data.results
            state.lessInvoices = state.moreInvoices.slice(0, state.lessShowLine)
        })
        return {
            ...toRefs(state),
            getFormattedDate,
            showMoreInvoices,
        }
    }
}
