import {getCollaboratorActivities, dealCollaboratorActivities } from '../services/activity'
import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted} from 'vue'
import { useStore } from "vuex"

export default {
    name: "OverviewCollaboratorActivity",
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

        const goToAccess = () => {
            router.push({ path: `/apps/${props.appDetail.id}/access` })
        }

        onMounted(async () => {
            var currentCluster = store.getters.currentCluster
            const res =  await getCollaboratorActivities(currentCluster.uuid, params.id)
            state.activities = dealCollaboratorActivities(res)
        })


        return {
            ...toRefs(state),
            goToAccess
        }

    }
}
