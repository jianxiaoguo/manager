import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted , computed} from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterAppDetail from "../components/ClusterAppDetail.vue";
import NavBoxAppDetailMenu from "../components/NavBoxAppDetailMenu.vue"
import MainNav from "../components/MainNav.vue";
import AccessCollaboratorEdit from "../components/AccessCollaboratorEdit.vue";
import { getAppAccesses, dealAppAccesses } from "../services/access"
import { useStore } from "vuex"

export default {
    name: "AppDetailAccess",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-app-detail': ClusterAppDetail,
        'nav-box-app-detail-menu': NavBoxAppDetailMenu,
        'main-nav': MainNav,
        'access-collaborator-edit': AccessCollaboratorEdit
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            appDetail: Object,
            accesses: [],
            isShowEdit: false,
            editAccess: null
        })

        const showEdit = (access) => {
            if (access) {
                state.editAccess = access
            }
            state.isShowEdit = true
        }

        const fetchAccesses = async () => {
            var currentCluster = store.getters.currentCluster
            state.appDetail = store.getters.currentApp
            let accessData = await getAppAccesses(currentCluster.uuid, params.id)
            state.accesses = accessData ? dealAppAccesses(state.appDetail, accessData) : null
        }

        const closeEdit = async () => {
            state.editAccess = null
            state.isShowEdit = false
            await fetchAccesses()
        }

        onMounted(async () => {
            await fetchAccesses()
        })

        return {
            ...toRefs(state),
            showEdit,
            closeEdit
        }
    },
}
