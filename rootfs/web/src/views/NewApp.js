import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import { reactive, toRefs, onMounted } from 'vue'
import { useStore } from "vuex";
import { createApp } from "../services/app"
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

export default {
    name: "NewApp",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
    },
    setup() {
        const state = reactive({
            isMenuActived: false,
            clusters: [],
            selectedClusterId: '',
            appName: ''
        })
        const store = useStore()
        const router = useRouter()
        const createNewApp = () => {
            createApp(state.selectedClusterId, state.appName).then(res=>{
                ElMessage({
                    message: 'Create new app ok.',
                    type: 'success',
                })
                router.push({ path: '/apps'})
            })
        }

        onMounted(async () => {
            state.clusters = store.getters.clusters
            state.selectedClusterId = store.getters.currentCluster.uuid
        })

        return {
            ...toRefs(state),
            createNewApp
        }
    },

    mounted() {
        let _this = this
        document.addEventListener('click', function (e) {
            // 下面这句代码是获取 点击的区域是否包含你的菜单，如果包含，说明点击的是菜单以外，不包含则为菜单以内
            if (e.target.id !== 'menu-select-group') {
                _this.isMenuActived = false
            }

        })
    }
}
