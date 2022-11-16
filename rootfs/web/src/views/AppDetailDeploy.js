import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted } from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterSelectAppDetail from "../components/ClusterSelectAppDetail.vue";
import NavBoxAppDetailMenu from "../components/NavBoxAppDetailMenu.vue"
import MainNav from "../components/MainNav.vue";
import DeployDryccGit from "../components/DeployDryccGit.vue";
import DeployDryccImage from "../components/DeployDryccImage.vue";
import { useStore } from "vuex"

export default {
    name: "AppDetailDeploy",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-app-select': ClusterSelectAppDetail,
        'nav-box-app-detail-menu': NavBoxAppDetailMenu,
        'main-nav': MainNav,
        'deploy-drycc-git': DeployDryccGit,
        'deploy-drycc-image': DeployDryccImage
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params

        const state = reactive({
            cluster: Object,
            appDetail: Object,
            depolyType: params.deployType,
        })

        const goToDryccGit = () => {
            router.push({ path: `/apps/${params.id}/deploy/drycc-git` })
            state.depolyType = 'drycc-git'
        }

        const goToDryccImage = () => {
            router.push({ path: `/apps/${params.id}/deploy/drycc-image` })
            state.depolyType = 'drycc-image'
        }

        if (!state.depolyType) {
            goToDryccGit()
        }

        onMounted(async () => {
            state.appDetail = store.getters.currentApp
            state.cluster = store.getters.currentCluster
        })

        return {
            ...toRefs(state),
            goToDryccGit,
            goToDryccImage
        }
    },
}
