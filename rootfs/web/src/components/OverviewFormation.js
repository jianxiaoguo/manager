import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted} from 'vue'
import { getAppProcesses, dealAppProcesses } from "../services/process";
import { useStore } from "vuex"

export default {
    name: "OverviewFormation",
    props: {
        appDetail: [Object, Function]
    },
    setup(props) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            processes: []
        })

        const goToResources = () => {
            router.push({ path: `/apps/${props.appDetail.id}/resources` })
        }

        onMounted(async () => {
            var currentCluster = store.getters.currentCluster
            var res =  await getAppProcesses(currentCluster.uuid, params.id)
            state.processes = dealAppProcesses(res)
        })

        return {
            ...toRefs(state),
            goToResources
        }

    }
}
