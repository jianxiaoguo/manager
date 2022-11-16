import {onMounted, reactive, toRefs} from "vue";
import { getUser, dealUser } from '../services/user'
import {getBalance} from '../services/fund'

export default {
    name: "AccountSettingProfile",
    setup() {
        const state = reactive({
            user :{
                username: "",
                email: ""
            },
            balance: {
                amount: 0,
                status: "",
                created: "",
                updated: "",
            },
        })

        onMounted(async () => {
           
            let res = await getUser()
            state.user = dealUser(res)
            res = await getBalance()
            state.balance = res.data ? res.data : 0
        })
        return {
            ...toRefs(state),
        }
    }
}
