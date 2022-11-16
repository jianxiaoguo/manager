import { useRouter } from 'vue-router'
import { reactive, toRefs, onMounted } from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import {getApplogs,dealApplogs} from "../services/logs";
import { useStore } from "vuex"

export default {
    name: "AppDetailLogs",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            appLogs: [],
        })
        const saveLogs = () => {
            const blob = new Blob([state.appLogs], { type: "application/octet-stream" });
            const elink = document.createElement("a");
            elink.download = "logs.txt";
            elink.style.display = "none";
            elink.href = URL.createObjectURL(blob);
            document.body.appendChild(elink);
            elink.click();
            URL.revokeObjectURL(elink.href); // 释放URL 对象
            document.body.removeChild(elink);
        }
        onMounted(async () => {
            var currentCluster = store.getters.currentCluster
            const res = await getApplogs(currentCluster.uuid, params.id)
            state.appLogs = res.data ? dealApplogs(res) : []
        })

        return {
            ...toRefs(state),
            saveLogs
        }
    },
}
