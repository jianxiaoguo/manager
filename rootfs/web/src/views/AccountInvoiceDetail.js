import { ref, reactive, toRefs, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { getSettings } from '../services/settings'
import { getConsumerTaxInfo } from '../services/tax'
import {getInvoice, getInvoiceAddress, getPaymentCard} from "../services/bill";


export default {
    name: "AccountInvoiceDetail",
    setup(props) {
        const state = reactive({
            invoice: {
                period: ref(""),
                price: ref(""),
                discount: ref(""),
                tax: ref(""),
                total: ref(""),
                bill_summary: ref([]),
                payment_methods: ref([]),
            },
            address: ref(""),
            fromDate: ref(""),
            toDate: ref(""),
            consumer: {
                no: "",
                provider: {
                    no: "",
                    rate: 0,
                }
            },
            fromCompany: {
                name: "Doopai",
                email: "",
                phone: "",
                address: {
                    line1: "",
                    line2: "",
                    city: "",
                    state: "",
                    country: "",
                    postcode: "",
                }
            },
            paymentCard: ref(""),
        })
        const router = useRouter()
        const params = router.currentRoute.value.params

        const getFormattedDate = (date) => {
            var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            return `${date.getDay()} ${months[date.getMonth()]} ${date.getFullYear()}`
        }

        onBeforeMount(async () => {
            var res = await getInvoice(params.id)
            state.invoice = res.data
            res = await getInvoiceAddress()
            if(Object.keys(res.data).length != 0) {
                state.address = res.data
            }
            res = await getPaymentCard()
            if(Object.keys(res.data).length != 0) {
                state.paymentCard = res.data
            }
            res = await getSettings()
            state.fromCompany = res.data.billing_details
            res = await getConsumerTaxInfo()
            state.consumer = res.data
            
            var date = new Date(state.invoice.period * 1000)
            state.fromDate = getFormattedDate(date)
            date.setMonth(date.getMonth() + 1)
            state.toDate = getFormattedDate(date)
        })

        return {
            ...toRefs(state),
        }

    }
}
