import { watch, onMounted, reactive, toRefs} from "vue";
import { useRouter } from 'vue-router'
import { useStore } from "vuex";
import {dealUser, getUser, postLogout, getMessages} from "../services/user";

export default {
    name: "UserMenu",
    data() {
        return {
            isMenuActived: false
        }
    },
    methods: {
        openOrCloseMenu() {
            this.isMenuActived = !this.isMenuActived;
        }
    },
    setup() {
        const state = reactive({
            user :{
                username: null,
                email: null,
                is_superuser: null
            },
            unreadCount: 0,
        })
        const store = useStore()
        const router = useRouter()
        const logout = () => {
            postLogout().then(res=>{
                localStorage.clear()
                document.cookie = ''
                router.push({ path: '/login'})
                location.replace(process.env.VUE_APP_BASE_URL + "/login/drycc/")
            })
        }
        onMounted(async () => {
            if (store.getters.user){
                state.user = store.getters.user
            }else {
                const res = await getUser()
                state.user = dealUser(res)
                store.dispatch('setUser', state.user)
            }

            let res = await getMessages(true)
            state.unreadCount = res.data.count
            store.dispatch('setUnreadMessageCount', state.unreadCount)
        })

        watch(()=>store.getters.unreadMessageCount, async()=>{
            state.unreadCount = store.getters.unreadMessageCount
        })

        return {
            ...toRefs(state),
            logout
        }
    },
    mounted() {
        let _this = this
        document.addEventListener('click', function (e) {
            // 下面这句代码是获取 点击的区域是否包含你的菜单，如果包含，说明点击的是菜单以外，不包含则为菜单以内
            if (e.target.id !== 'menu-account') {
                _this.isMenuActived = false
            }
        })
    }
}
