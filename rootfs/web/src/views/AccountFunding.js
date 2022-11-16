import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import { useRouter } from 'vue-router'
import { watch, ref, reactive, toRefs, onMounted } from 'vue'
import {dealAccountFundingList, getAccountFundingList} from "../services/fund";


export default {
    name: "AccountFunding",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
    },
    setup(props) {
        const router = useRouter()
        const state = reactive({
            direction: ref(''),
            directionOptions: ref([
                {
                    value: 1,
                    label: 'income'
                },
                {
                    value: 2,
                    label: 'expense'
                }
            ]),
            tradingType: ref(''),
            tradingTypeOptions: ref([
                {
                    value: 1,
                    label: 'account adjustment'
                },
                {   
                    value: 2,
                    label: 'recharge'
                },
                {   
                    value: 4,
                    label: 'refund'
                },
                {
                    value: 5,
                    label: 'withdrawal'
                },
                {
                    value: 6,
                    label: 'consumption'
                },
            ]),
            period: ref(''),
            fundingList: ref([]),
            pageSize: 30,
            page: 1,
            count: 0,
        })
        const fetchFundFlow = async() => {
            let period = state.period ? state.period.getTime()/1000 : ''
            let res = await getAccountFundingList(state.tradingType, state.direction, period, state.pageSize, state.pageSize * (state.page - 1))
            if(res.data) {
                state.count = res.data.count
                state.fundingList = dealAccountFundingList(res)
            }
        }

        watch(()=>state.period,async()=>{
            state.page = 1
            await fetchFundFlow()
        })
        watch(()=>state.tradingType,async()=>{
            state.page = 1
            await fetchFundFlow()
        })
        watch(()=>state.direction,async()=>{
            state.page = 1
            await fetchFundFlow()
        })

        const goToAccountSetting = () => {
            router.push({ path: `/account` })
        }

        const goToAccountFunding = () => {
            router.push({ path: `/account/funding` })
        }

        const goToAccountBilling = () => {
            router.push({ path: `/account/billing` })
        }

        const pageCurrentChange = async(e) => {
            state.page = e
            await fetchFundFlow()
        }

        onMounted(async () => {
            state.page = 1
            await fetchFundFlow()
        })

        return {
            ...toRefs(state),
            goToAccountSetting,
            goToAccountFunding,
            goToAccountBilling,
            pageCurrentChange,
        }

    }
}
