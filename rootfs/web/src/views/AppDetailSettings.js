import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted } from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterAppDetail from "../components/ClusterAppDetail.vue";
import NavBoxAppDetailMenu from "../components/NavBoxAppDetailMenu.vue"
import MainNav from "../components/MainNav.vue";
import SettingAppInfo from "../components/SettingAppInfo.vue";
import SettingDeleteApp from "../components/SettingDeleteApp.vue";
import SettingDomains from "../components/SettingDomains.vue";
import SettingTransferOwnership from "../components/SettingTransferOwnership.vue";
import { useStore } from "vuex";

export default {
    name: "AppDetailSettings",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-app-detail': ClusterAppDetail,
        'nav-box-app-detail-menu': NavBoxAppDetailMenu,
        'main-nav': MainNav,
        'setting-app-info': SettingAppInfo,
        'setting-domains': SettingDomains,
        'setting-transfer-ownership': SettingTransferOwnership,
        'setting-delete-app': SettingDeleteApp
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
