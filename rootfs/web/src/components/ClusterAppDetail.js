import { ref, reactive, toRefs, onBeforeMount} from 'vue'
import { getCsrf } from "../services/user";
import { getClusters } from "../services/cluster";
import { useStore } from "vuex";


export default {
    name: "ClusterAppDetail",
    props: {
        appDetail: [Object, Function],
    },
    setup() {
        const store = useStore()
        const state = reactive({
            currentCluster: ref('')
        })
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
            ...toRefs(state)
        }
    },
}
