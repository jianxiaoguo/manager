import { reactive, toRefs, onMounted} from 'vue'
import ClusterSelect from "../components/ClusterSelect.vue";

export default {
    name: "ClusterSelectAppDetail",
    components: {
        'cluster-select': ClusterSelect,
    },
    props: {
        appDetail: [Object, Function]
    },
    setup() {
        const state = reactive({
        })

        return {
            ...toRefs(state)
        }
    },
}
