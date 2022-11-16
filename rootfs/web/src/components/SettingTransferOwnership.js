import {useRouter} from "vue-router";
import {reactive, toRefs} from "vue";
import {updateApp} from "../services/app";
import { ElMessageBox, ElMessage } from 'element-plus'
import { useStore } from "vuex"

export default {
    name: "SettingTransferOwnership",
    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            username: null
        })
        const transferOwnership = async () => {
            var currentCluster = store.getters.currentCluster
            ElMessageBox.confirm('Are you sure to transfer ownership this app?').then(async () => {
                updateApp(currentCluster.uuid, params.id, state.username).then(res => {
                    if (res.status == 200) {
                        ElMessage({
                            message: 'Transfer ownership ok.',
                            type: 'success',
                        })
                        router.push({ path: `/apps`})
                    } else {
                        ElMessage.error(res.data)
                    }
                })
            }).catch(() => {
                console.log("Ignore delete app operation", params.id)
            })
        }
        return {
            ...toRefs(state),
            transferOwnership,
        }
    },
}
