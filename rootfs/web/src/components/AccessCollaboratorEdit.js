import { reactive, ref, toRefs } from 'vue'
import { addAppAccesses, deleteAppAccesses, updateAppAccesses } from "../services/access";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ElMessage } from 'element-plus'

export default {
    name: "AccessCollaboratorEdit",
    props: {
        appDetail: [Object, Function],
        editAccess: [Object, Function]
    },
    setup(props, context) {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            username: ref(''),
            permissions: ref([])
        })
        
        if (props.editAccess) {
            state.username = props.editAccess.username
            state.permissions = props.editAccess.permissions
        }

        const canelEdit = () => {
            context.emit('closeEdit')
        }
        const savePerm = async () => {
            var currentCluster = store.getters.currentCluster
            var action = addAppAccesses
            if (props.editAccess) {
                action = updateAppAccesses
            }
            action(currentCluster.uuid, params.id, state.username, state.permissions).then(res=>{
                if (res.status >= 200  && res.status < 300) {
                    ElMessage({
                        message: 'OK',
                        type: 'success',
                    })
                    context.emit('closeEdit')
                }
            })
        }
        const deletePerm = async () => {
            var currentCluster = store.getters.currentCluster
            deleteAppAccesses(currentCluster.uuid, params.id, state.username).then(res=>{
                if (res.status == 204) {
                    ElMessage({
                        message: 'Delete perm ok',
                        type: 'success',
                    })
                    context.emit('closeEdit')
                }
            })
        }
        return {
            ...toRefs(state),
            canelEdit,
            savePerm,
            deletePerm
        }
    }
}
