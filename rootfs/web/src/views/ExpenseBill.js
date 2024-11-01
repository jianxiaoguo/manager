import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import { useRouter } from 'vue-router'
import { getAPPList, dealAPPList } from "../services/app";
import { getBillsSummary } from "../services/bill";
import { useStore } from "vuex";
import { reactive, toRefs, watch, ref} from 'vue'

export default {
    name: "ExpenseBill",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const state = reactive({
            period: ref(''),
            cluster: ref(''),
            clusterOptions: ref([]),
            app: ref(''),
            appOptions: ref([]),
            page: 1,
            pageSize: 30,
            count: 0,
            billList: ref([])
        })

        const fetchBillSummary = async() => {
            let period = state.period ? state.period.getTime()/1000 : ''
            let res = await getBillsSummary(state.cluster, state.app, period, null, state.pageSize, state.pageSize * (state.page - 1))
            if(res.data){
                state.count = res.data.count
                state.billList = res.data.results
            }
        }

        watch(()=>state.cluster, async()=>{
            if(!state.cluster){
                state.app = ''
            }
            await fetchBillSummary()
        })

        watch(()=>state.app, async()=>{
            await fetchBillSummary()
        })

        watch(()=>state.period, async()=>{
            await fetchBillSummary()
        })

        const pageCurrentChange = async(e) => {
            state.page = e
            await fetchBillSummary()
        }
        
        const filterAppOptions = async(query) => {
            let res = await getAPPList(state.cluster, query)
            if(res.data) {
                state.appOptions = dealAPPList(res)
                console.log(state.appOptions)
            }
        }

        const goToExpenseBills = () => {
            router.push({ path: `/expense-bills` })
        }

        const goToExpenseBillsDetails = () => {
            router.push({ path: `/expense-bills/details` })
        }
        onBeforeMount(async()=>{
            await fetchBillSummary()
            state.clusterOptions = store.getters.clusters
        })

        return {
            ...toRefs(state),
            filterAppOptions,
            goToExpenseBills,
            goToExpenseBillsDetails,
            pageCurrentChange,
        }

    }
}
