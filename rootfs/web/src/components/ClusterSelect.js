import { reactive, toRefs, onBeforeMount, ref} from 'vue'
import { useRouter } from 'vue-router'
import { getClusters } from "../services/cluster";
import { getCsrf } from "../services/user";
import { useStore } from "vuex";

export default {
    name: "ClusterSelect",
    setup() {
        const store = useStore()
        const router = useRouter()
        const state = reactive({
            clusters: ref([]),
            currentCluster: ref(''),
        })

        const changeCluster = (cluster) => {
            state.currentCluster = cluster
            store.dispatch("setCurrentCluster", cluster)
            router.replace({ path: '/'})
        }


        onBeforeMount(async () => {
            const token =await getCsrf()
            sessionStorage.setItem('csrftoken', token.data.token)

            state.clusters = await getClusters()
            store.dispatch("setClusters", state.clusters)

            if(!store.getters.currentCluster && state.clusters.length > 0){
                state.currentCluster = state.clusters[0]
                store.dispatch("setCurrentCluster", state.currentCluster)
            }else{
                state.currentCluster = store.getters.currentCluster
            }
        })
        return {
            ...toRefs(state),
            changeCluster
        }
    },
}
