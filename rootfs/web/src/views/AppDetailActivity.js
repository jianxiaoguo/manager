import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted , provide} from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterSelectAppDetail from "../components/ClusterSelectAppDetail.vue";
import NavBoxAppDetailMenu from "../components/NavBoxAppDetailMenu.vue"
import MainNav from "../components/MainNav.vue";
import ActivityRollBack from "../components/ActivityRollBack.vue";
import { useStore } from "vuex"
import { getAppActivities, dealAppActivities, postAppActivitieRollback } from "../services/activity";
import { ElMessage } from 'element-plus'

export default {
    name: "AppDetailActivity",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-app-select': ClusterSelectAppDetail,
        'nav-box-app-detail-menu': NavBoxAppDetailMenu,
        'main-nav': MainNav,
        'activity-roll-back': ActivityRollBack
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            appDetail: Object,
            activities: [],
            isShowRollBack: false,
            rollBackIndex: 0
        })

        onMounted(async () => {
            var currentCluster = store.getters.currentCluster
            state.appDetail = store.getters.currentApp
            const activityData = await getAppActivities(currentCluster.uuid, params.id)

            state.activities = activityData.data ? dealAppActivities(activityData) : null
        })

        const closeRollBack = () => {
            state.rollBackIndex = 0
            state.isShowRollBack = false
        }

        const openRollBack = async (v) => {
            state.rollBackVersion = v
            state.isShowRollBack = true
            var currentCluster = store.getters.currentCluster
            postAppActivitieRollback(currentCluster.uuid, params.id, v).then(res=>{
                if (res.status == 201){
                    ElMessage({
                        message: 'Post app activitie rollback ok.',
                        type: 'success',
                    })
                }
            })
        }


        return {
            ...toRefs(state),
            openRollBack,
            closeRollBack
        }
    },
}
