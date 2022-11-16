import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted} from 'vue'
import { getAppAddons, dealAppAddons } from "../services/addons";
import { getAppProcesses, dealAppProcesses } from "../services/process";
import { useStore } from "vuex"

export default {
    name: "ResourcesDyno",
    props: {
        appDetail: [Object, Function]
    },
    setup(props) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            addons: [],
            processes: []
        })

        const goToResources = () => {
            router.push({ path: `/apps/${props.appDetail.id}/resources` })
        }

        const editProcess = (pro) => {
            pro.disabled = false
        }

        const closeEditProcess = (pro) => {
            pro.disabled = true
        }

        const editProcessStatus = (pro) => {
            if (!pro.disabled) {
                if (pro.status === 0) {
                    pro.status = 1
                } else {
                    pro.status = 0
                }
            }

        }

        const confirmEditProcess = (pro) => {
            pro.disabled = true
        }

        onMounted(async () => {
            var currentCluster = store.getters.currentCluster
            const res =  await getAppAddons(currentCluster.uuid, params.id)

            state.addons = dealAppAddons(res)
            const processData =  await getAppProcesses(currentCluster.uuid, params.id)
            state.processes = dealAppProcesses(processData)
        })

        return {
            ...toRefs(state),
            goToResources,
            editProcess,
            closeEditProcess,
            confirmEditProcess,
            editProcessStatus
        }

    }
}
