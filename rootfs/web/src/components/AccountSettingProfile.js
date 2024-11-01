import {onBeforeMount, reactive, ref, toRefs} from "vue";
import { getUser, dealUser } from '../services/user'
import {getBalance} from '../services/fund'

const zeroBalance = {amount: 0, status: "", created: "", updated: ""}

export default {
    name: "AccountSettingProfile",
    setup() {
        const state = reactive({
            user :ref({
                username: "",
                email: ""
            }),
            balance: ref(zeroBalance),
        })
        onBeforeMount(async () => {
            let res = await getUser()
            state.user = dealUser(res)
            res = await getBalance()
            state.balance = res.data ? res.data : zeroBalance
        })
        return {
            ...toRefs(state),
        }
    }
}
