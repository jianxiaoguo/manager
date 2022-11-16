import { reactive, toRefs, onMounted } from 'vue'
import { useStore } from "vuex"

export default {
    name: "DeployDryccImage",
    setup() {
        const store = useStore()
        const state = reactive({
            cluster: Object,
            appDetail: Object,
        })

        onMounted(async () => {
            state.cluster = store.getters.currentCluster
            state.appDetail = store.getters.currentApp
        })
        return {
            ...toRefs(state),
        }
    }
}