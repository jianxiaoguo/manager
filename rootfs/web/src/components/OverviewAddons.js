import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted} from 'vue'
import { getAppAddons, dealAppAddons } from "../services/addons";
import { useStore } from "vuex"

export default {
    name: "OverviewAddons",
    props: {
        appDetail: [Object, Function]
    },
    setup(props) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            addons: []
        })

        const goToResources = () => {
            router.push({ path: `/apps/${props.appDetail.id}/resources` })
        }

        onMounted(async () => {
            var currentCluster = store.getters.currentCluster
            const res =  await getAppAddons(currentCluster.uuid, params.id)

            state.addons = dealAppAddons(res)
        })

        return {
            ...toRefs(state),
            goToResources
        }

    }
}
