import { useRouter } from 'vue-router'
import { reactive, toRefs, onBeforeMount } from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterSelectAppDetail from "../components/ClusterSelectAppDetail.vue";
import NavBoxAppDetailMenu from "../components/NavBoxAppDetailMenu.vue"
import MainNav from "../components/MainNav.vue";
import OverviewAppInfo from "../components/OverviewAppInfo.vue";
import OverviewAddons from "../components/OverviewAddons.vue";
import OverviewFormation from "../components/OverviewFormation.vue";
import OverviewVolume from "../components/OverviewVolume.vue";
import OverviewCollaboratorActivity from "../components/OverviewCollaboratorActivity.vue";
import OverviewLatestActivity from "../components/OverviewLatestActivity.vue";
import { useStore } from "vuex";

export default {
    name: "AppDetailOverview",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-app-select': ClusterSelectAppDetail,
        'nav-box-app-detail-menu': NavBoxAppDetailMenu,
        'main-nav': MainNav,
        // 'overview-metrics': OverviewMetrics,
        'overview-appinfo': OverviewAppInfo,
        'overview-addons': OverviewAddons,
        'overview-volume': OverviewVolume,
        'overview-formation': OverviewFormation,
        'overview-collaborator-activity': OverviewCollaboratorActivity,
        'overview-latest-activity': OverviewLatestActivity
    },

    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            appDetail: Object,
        })
        onBeforeMount(async () => {
            state.appDetail = store.getters.currentApp
        })
        return {
            ...toRefs(state)
        }
    },
}
