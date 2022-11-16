import { useRouter } from 'vue-router'
import { toRefs, ref } from 'vue'
import { useStore } from "vuex";


export default {
    name: "OneApp",
    props: {
        app: ref(Object),
    },
    setup(props) {
        const app = props.app
        const store = useStore()
        const router = useRouter()
        const goToAppDetail = () => {
            store.dispatch('setCurrentApp', app)
            router.push({ path: `/apps/${app.id}` })
        }
        return {
            ...toRefs(app),
            goToAppDetail,
        }
    },
}
