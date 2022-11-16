
import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted} from 'vue'
import { getVolumes, dealVolumes } from "../services/volume";
import { useStore } from "vuex"

export default {
    name: "ResourcesVolume",
    props: {
        appDetail: [Object, Function]
    },
    setup(props) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            volumes: []
        })

        const goToResources = () => {
            router.push({ path: `/apps/${props.appDetail.id}/resources` })
        }

        onMounted(async () => {
            var currentCluster = store.getters.currentCluster
            const data =  await getVolumes(currentCluster.uuid, params.id)
            state.volumes = dealVolumes(data)
        })

        return {
            ...toRefs(state),
            goToResources
        }

    }
}
