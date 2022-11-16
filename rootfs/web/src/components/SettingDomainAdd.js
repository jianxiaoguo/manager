import { reactive, toRefs } from 'vue'
import { addAppDomains, deleteAppDomains } from "../services/domain";
import { useRouter } from "vue-router";
import { ElMessage } from 'element-plus'
import { useStore } from "vuex"

export default {
    name: "SettingDomainAdd",
    props: {
        appDetail: [Object, Function],
        editAccess: [Object, Function]
    },
    setup(props, context) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        
        const state = reactive({
            domain: null,
        })

        const canelEdit = () => {
            context.emit('closeEdit', { hasDomainEdit: false })
        }
        const addAppDomain = async () => {
            var currentCluster = store.getters.currentCluster
            addAppDomains(currentCluster.uuid, params.id, state.domain).then(res=>{
                if (res.status == 201) {
                    ElMessage({
                        message: 'Add app domain ok.',
                        type: 'success',
                    })
                    context.emit('closeEdit', { hasDomainEdit: true })
                }
            })
        }
        const deleteAppDomain = async () => {
            var currentCluster = store.getters.currentCluster
            deleteAppDomains(currentCluster.uuid, params.id, state.domain).then(res=>{
                if (res.status == 204) {
                    ElMessage({
                        message: 'Delete app domain ok.',
                        type: 'success',
                    })
                    context.emit('closeEdit')
                }
            })
        }
        return {
            ...toRefs(state),
            canelEdit,
            addAppDomain,
            deleteAppDomain
        }
    }
}
