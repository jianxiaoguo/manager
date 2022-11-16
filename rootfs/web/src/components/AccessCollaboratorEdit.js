import { reactive, toRefs } from 'vue'
import { addAppAccesses, deleteAppAccesses } from "../services/access";
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
            username: null,
            // newUser: null
        })
        
        if (props.editAccess) {
            state.username = props.editAccess.username
        }

        const canelEdit = () => {
            context.emit('closeEdit')
        }
        const addPerm = async () => {
            var currentCluster = store.getters.currentCluster
            addAppAccesses(currentCluster.uuid, params.id, state.username).then(res=>{
                if (res.status == 201) {
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
            addPerm,
            deletePerm
        }
    }
}
