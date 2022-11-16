import { useRouter } from "vue-router";
import { deleteApp } from "../services/app";
import { useStore } from "vuex"
import { ElMessageBox, ElMessage } from 'element-plus'

export default {
    name: "SettingDeleteApp",
    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const deleteAppBTN = async () => {
            var currentCluster = store.getters.currentCluster
            ElMessageBox.confirm('Are you sure to delete this app?').then(async () => {
                deleteApp(currentCluster.uuid, params.id).then(res=>{
                    router.push({ path: '/apps'})
                    ElMessage({
                        message: 'Delete app ok.',
                        type: 'success',
                    })
                })
            }).catch(() => {
                console.log("Ignore delete app operation", params.id)
            })
        }
        return {
            deleteAppBTN
        }
    },
}
