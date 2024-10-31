import {useRouter} from 'vue-router'
import {reactive, toRefs, onMounted} from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterAppDetail from "../components/ClusterAppDetail.vue";
import NavBoxAppDetailMenu from "../components/NavBoxAppDetailMenu.vue"
import MainNav from "../components/MainNav.vue";
import ResourcesDyno from "../components/ResourcesDyno.vue";
import ResourcesAddons from "../components/ResourcesAddons.vue";
import ResourcesVolume from "../components/ResourcesVolume.vue";
import { useStore } from "vuex";

export default {
    name: "AppDetailResources",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-app-detail': ClusterAppDetail,
        'nav-box-app-detail-menu': NavBoxAppDetailMenu,
        'main-nav': MainNav,
        'resources-dyno': ResourcesDyno,
        'resources-addons': ResourcesAddons,
        'resources-volume': ResourcesVolume
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const state = reactive({
            appDetail: Object
        })

        onMounted(async () => {
            state.appDetail = store.getters.currentApp
        })

        return {
            ...toRefs(state)
        }
    },
}
