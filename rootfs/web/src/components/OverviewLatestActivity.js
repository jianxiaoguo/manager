import { getAppActivities, dealAppActivities } from '../services/activity'
import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted} from 'vue'
import { useStore } from "vuex"

export default {
    name: "OverviewLatestActivity",
    props: {
        appDetail: [Object, Function]
    },
    setup(props) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            activities: []
        })

        const goToActivity = () => {
            router.push({ path: `/apps/${props.appDetail.id}/activity` })
        }

        onMounted(async () => {
            var currentCluster = store.getters.currentCluster
            const res = await getAppActivities(currentCluster.uuid, params.id)

            state.activities = res.data ? dealAppActivities(res) : []
        })

        return {
            ...toRefs(state),
            goToActivity
        }

    }
}
