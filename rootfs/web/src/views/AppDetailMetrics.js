import { useRouter } from 'vue-router'
import { reactive, toRefs, onBeforeMount, ref, watch } from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterAppDetail from "../components/ClusterAppDetail.vue";
import NavBoxAppDetailMenu from "../components/NavBoxAppDetailMenu.vue"
import MainNav from "../components/MainNav.vue";
import MetricMemory from "../components/MetricMemory.vue";
import MetricNetwork from "../components/MetricNetwork.vue";
import MetricCpu from "../components/MetricCpu.vue";
import { useStore } from "vuex";
import { getAppProcessTypes, dealProcessTypes } from "../services/process";
import { getMetricStatus } from "../services/metric";

export default {
    name: "AppDetailMetrics",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-app-detail': ClusterAppDetail,
        'nav-box-app-detail-menu': NavBoxAppDetailMenu,
        'main-nav': MainNav,
        'metric-memory': MetricMemory,
        'metric-network': MetricNetwork,
        'metric-cpu': MetricCpu
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            interval: ref('5'),
            appDetail: Object,
            processTypes: Array,
            currentProcess: ref(''),
            metricCpus: ref(''),
            metricMemory: ref(''),
            metricReceiveNetworks : ref(''),
            metricTransmitNetworks : ref(''),
        })

        const fetchMetric = async () =>{
            var currentCluster = store.getters.currentCluster
            let res = await getMetricStatus(
                currentCluster.uuid,
                params.id, state.currentProcess, state.interval)
            if(res.data){
                state.metricCpus = JSON.stringify(res.data.usage.cpus)
                state.metricMemory = JSON.stringify(res.data.usage.memory)
                state.metricReceiveNetworks = JSON.stringify(res.data.usage.networks.receive)
                state.metricTransmitNetworks = JSON.stringify(res.data.usage.networks.transmit)
            }
        }
        watch(()=>state.currentProcess,async()=>{
            router.push({ path: `/apps/${params.id}/metrics/processes/${state.currentProcess}` })
            await fetchMetric()
        })
        watch(() => state.interval, async()=>{
            await fetchMetric()
        })
        onBeforeMount( async () => {
            var currentCluster = store.getters.currentCluster
            state.appDetail = store.getters.currentApp
            let res = await getAppProcessTypes(currentCluster.uuid, params.id)
            state.processTypes = res.data ? dealProcessTypes(res) : []
            if (state.processTypes.length > 0) {
                if (!params.processType) {
                    state.currentProcess = state.processTypes[0].name
                    router.push({path: `/apps/${params.id}/metrics/processes/${state.currentProcess}`})
                } else {
                    const l = state.processTypes.filter(item => {
                        if (item.name.includes(params.processType)) {
                            return item
                        }
                    })
                    if (l.length > 0) {
                        state.currentProcess = l[0].name
                    } else {
                        state.currentProcess = state.processTypes[0].name
                    }
                }
                await fetchMetric()
            }
        })
        return {
            ...toRefs(state),
        }
    },
}
