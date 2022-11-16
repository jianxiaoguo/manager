import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import { ElMessageBox } from 'element-plus'
import {ref, toRefs,onMounted, reactive} from "vue";
import { useStore } from "vuex";
import {getMessages, deleteMessage as _deleteMessage, markAsReadMessage} from "../services/user";

export default {
    name: "AccountNotifications",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
    },
    setup() {
        const state = reactive({
            unread: '',
            messages: ref([]),
            messageDetail: ref(''),
            showMessageDetail: ref(false),
            pageSize: 30,
            page: 1,
            count: 0,
            unreadMessageCount: 0,
        })
        const store = useStore()
        const syncCanMarkAllAsRead = () => {
            state.unreadMessageCount = 0
            for(let index in state.messages) {
                let message = state.messages[index]
                if(message.unread) {
                    state.unreadMessageCount += 1
                }
            }
            if(store.getters.unreadMessageCount < state.unreadMessageCount){
                store.dispatch('setUnreadMessageCount', state.unreadMessageCount)
            }
        }

        const markAsRead = async (message) => {
            if(message.unread) {
                let res = await markAsReadMessage(message.uuid)
                if(res.status == 204) {
                    message.unread = false
                    syncCanMarkAllAsRead()
                    var index = state.messages.indexOf(message)
                    if(state.unread === 'true' && index >= 0) {
                        state.messages.splice(index, 1)
                    }
                    store.dispatch('setUnreadMessageCount', store.getters.unreadMessageCount - 1)
                }
            }
        }

        const openMessage = async (message) => {
            state.messageDetail = message.body
            state.showMessageDetail = true
            await markAsRead(message)
        }

        const fetchMessage = async () => {
            let res = await getMessages(state.unread, state.pageSize, state.pageSize * (state.page - 1))
            if(res.data){
                state.count = res.data.count
                state.messages = res.data.results
                syncCanMarkAllAsRead()
            }
        }

        const pageCurrentChange = async(e) => {
            state.page = e
            await fetchMessage()
        }

        const markCurrentPageAsRead = async() => {
            for(let index in state.messages) {
                let message = state.messages[index]
                await markAsRead(message)
            }
        }

        const deleteMessage = async(message) => {
            ElMessageBox.confirm('Are you sure to delete this message?').then(async () => {
                await _deleteMessage(message.uuid)
                state.page = 1
                await fetchMessage()
            }).catch(() => {
                console.log("Ignore delete message operation", message)
            })

        }

        const unreadChange = async(unread) => {
            state.unread = unread
            state.page = 1
            await fetchMessage()
        }

        onMounted(async () => {
            await fetchMessage()
        })
        return {
            ...toRefs(state),
            openMessage,
            unreadChange,
            deleteMessage,
            markCurrentPageAsRead,
            pageCurrentChange,
        }

    }
}
