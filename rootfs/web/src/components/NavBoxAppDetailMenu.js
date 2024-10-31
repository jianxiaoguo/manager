import { reactive, toRefs, onMounted} from 'vue'
import { useRouter } from 'vue-router'
import {getAppDomains, dealAppDomains} from "../services/domain"
import { useStore } from "vuex"

export default {
    name: "NavBoxAppDetailMenu",
    setup(props) {
        const router = useRouter()
        const store = useStore()
        const state = reactive({
            domain: String,
            isMenuActived: false,
        })

        const openOrCloseMenu = () => {
            state.isMenuActived = !state.isMenuActived
        }
        const goToLogs = () => {
            router.push({ path: `/apps/${props.appDetail.id}/logs` })
        }
        const fetchDomains = async () => {
            var currentApp = store.getters.currentApp
            var currentCluster = store.getters.currentCluster
            const res = await getAppDomains(currentCluster.uuid, currentApp.id)
            state.domain = res.data.count > 0 ? "http://" + dealAppDomains(res)[0].domain : null
        }
        onMounted(async () => {
            await fetchDomains()
        })
        return {
            ...toRefs(state),
            openOrCloseMenu,
            goToLogs
        }
    },
    mounted() {
        let _this = this
        document.addEventListener('click', function (e) {
            // 下面这句代码是获取 点击的区域是否包含你的菜单，如果包含，说明点击的是菜单以外，不包含则为菜单以内
            if (e.target.id !== 'nav-box-app-detail-menu') {
                _this.isMenuActived = false
            }

        })
    }
}
