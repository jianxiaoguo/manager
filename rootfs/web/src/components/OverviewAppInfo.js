import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted} from 'vue'
import { getAppDomains, dealAppDomains } from '../services/domain'
import { useStore } from "vuex"

export default {
    name: "OverviewAppInfo",
    props: {
        appDetail: [Object, Function]
    },
    setup(props) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            domains: [],
            ps: Object
        })
        onMounted(async () => {
            let currentCluster = store.getters.currentCluster
            let domainsData =  await getAppDomains(currentCluster.uuid, params.id)
            state.domains = domainsData ? dealAppDomains(domainsData): []
        })


        return {
            ...toRefs(state),
            // goToAccess
        }

    }
}
