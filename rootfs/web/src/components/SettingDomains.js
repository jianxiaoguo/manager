import SettingDomainAdd from "../components/SettingDomainAdd.vue";
import SettingDomainDelete from "../components/SettingDomainDelete.vue"
import NavBar from "../components/NavBar.vue";
import {useRouter} from "vue-router";
import {onMounted, reactive, toRefs} from "vue";
import {getAppDomains, dealAppDomains} from "../services/domain"
import { useStore } from "vuex"

export default {
    name: "SettingDomains",
    components: {
        'nav-bar': NavBar,
        'setting-domain-add': SettingDomainAdd,
        'setting-domain-delete': SettingDomainDelete
    },
    setup() {
        const store = useStore()
        const router = useRouter()
        const params = router.currentRoute.value.params
        const state = reactive({
            domain: Object,
            domains: [],
            isShowEdit: false,
            isShowDelete: false,
            editAccess: null
        })

        const showEdit = () => {
            state.isShowEdit = true
        }

        const closeEdit = (param) => {
            state.editAccess = null
            state.isShowEdit = false
            if (param.hasDomainEdit) {
                fetchDomains()
            }
        }
        const showDelete = (index) => {
            state.isShowDelete = true
            let domains = JSON.parse(JSON.stringify(state.domains));
            state.domain = domains.slice(index, index + 1)[0];
        }
        const closeDelete = (param) => {
            state.isShowDelete = false
            if (param.hasDomainDeleted) {
                fetchDomains()
            }
        }

        const fetchDomains = (async () => {
            var currentCluster = store.getters.currentCluster
            const res = await getAppDomains(currentCluster.uuid, params.id)
            state.domains = res ? dealAppDomains(res) : null
        })

        onMounted(async () => {
            await fetchDomains()
        })

        return {
            ...toRefs(state),
            showEdit,
            closeEdit,
            showDelete,
            closeDelete
        }
    },
}
