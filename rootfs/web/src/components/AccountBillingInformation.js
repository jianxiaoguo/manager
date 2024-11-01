import {onBeforeMount, reactive, ref, toRefs} from "vue";
import { ElMessage, ElMessageBox } from 'element-plus'
import {getBalance} from '../services/fund'
import AccountBillingPaymentCard from "../components/AccountBillingPaymentCard.vue"
import {publicKey, getBillsSummary, getPaymentCard, removePaymentCard} from '../services/bill'


export default {
    name: "AccountBillingInformation",
    components: {
        'account-bill-payment-card': AccountBillingPaymentCard
    },
    setup(props) {
        const state = reactive({
            usage: ref(0),
            amount: ref(0),
            publicKey: ref(''),
            paymentCard: ref(''),
            editPaymentCard: false,
        })

        const removePayment = async () => {
            ElMessageBox.confirm('Are you sure to delete this payment card?').then(async () => {
                removePaymentCard().then(res=>{
                    if (res.status == 204) {
                        ElMessage({
                            message: 'Delete app domain ok.',
                            type: 'success',
                        })
                        state.paymentCard = ref('')
                    }
                })
            }).catch(() => {
                console.log("Ignore delete app operation")
            })
        }

        const editPaymentCardAction = async () => {
            state.editPaymentCard = true
        }
        
        const closePaymentCardAction = async (params) => {
            state.editPaymentCard = false
            if(params.savePaymentCard) {
                let res = await getPaymentCard()
                if(Object.keys(res.data).length != 0) {
                    state.paymentCard = res.data
                }
            }
        }

        onBeforeMount(async () => {
            let res = await getPaymentCard()
            if(Object.keys(res.data).length != 0) {
                state.paymentCard = res.data
            }
            res = await getBillsSummary(null, null, null, "owner_id")
            if(res.data.count > 0){
                state.usage = res.data.results[0].price
            }
            res = await getBalance()
            state.amount = res.data ? res.data.amount : 0

            res = await publicKey()
            state.publicKey = res.data["public_key"]
        })
        return {
            ...toRefs(state),
            removePayment,
            editPaymentCardAction,
            closePaymentCardAction,
        }
    }
}
