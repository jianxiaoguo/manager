import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterSelect from "../components/ClusterSelect.vue";
import OneApp from "../components/OneApp.vue";
import { reactive, toRefs, onBeforeMount, ref, watch} from 'vue'
import { getAPPList, dealAPPList } from "../services/app";
import { useRouter } from 'vue-router'
import { useStore } from "vuex";
import { getCsrf } from "../services/user";

export default {
    name: "AppList",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-select': ClusterSelect,
        'one-app': OneApp,
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const state = reactive({
            clusters: ref([]),
            apps: ref([]),
            name: ref(''),
            pageSize: 30,
            page: 1,
            count: 0,
            currentCluster: ref(''),
        })
        const pageCurrentChange = async(e) => {
            state.page = e
            await fetchAppList()
        }
        const goToNewApp = () => {
            router.push({ path: '/new-app'})
        }

        const fetchAppList = async() => {
            let res = await getAPPList(state.currentCluster.uuid, state.name, state.pageSize, state.pageSize * (state.page - 1))
            if(res.data){
                state.count = res.data.count
                state.apps = dealAPPList(res)
            }
        }

        watch(()=>store.getters.currentCluster, async () => {
            state.currentCluster = store.getters.currentCluster
            state.page = 1
            await fetchAppList()
        })

        onBeforeMount(async () => {
            state.clusters = store.getters.clusters
            state.currentCluster = store.getters.currentCluster

            if(state.currentCluster){
                state.page = 1
                await fetchAppList()
            }
            getCsrf().then(res=>{
                sessionStorage.setItem('csrftoken', res.data.token)
            })
        })

        return {
            ...toRefs(state),
            goToNewApp,
            fetchAppList,
            pageCurrentChange,
        }
    },
}
