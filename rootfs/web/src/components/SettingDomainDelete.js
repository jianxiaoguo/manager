import { reactive, toRefs } from 'vue'
import { deleteAppDomains } from "../services/domain";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from 'element-plus'
import { useStore } from "vuex"

export default {
    name: "SettingDomainDelete",
    props: {
        domain: [Object, Function],
        appDetail: [Object, Function],
        editAccess: [Object, Function]
    },
    setup(props, context) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            domain: props.domain,
        })
        

        const canelDelete = () => {
            context.emit('closeDelete', { hasDomainDeleted: false })
        }
        const deleteAppDomain = async () => {
            var currentCluster = store.getters.currentCluster
            ElMessageBox.confirm('Are you sure to delete this domain?').then(async () => {
                deleteAppDomains(currentCluster.uuid, params.id, state.domain.domain).then(res=>{
                    if (res.status == 204) {
                        ElMessage({
                            message: 'Delete app domain ok.',
                            type: 'success',
                        })
                        context.emit('closeDelete', { hasDomainDeleted: true })
                    }
                })
            }).catch(() => {
                console.log("Ignore delete app operation", params.id)
            })
        }
        return {
            ...toRefs(state),
            canelDelete,
            deleteAppDomain
        }
    }
}
