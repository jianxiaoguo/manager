import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import { ref, toRefs , reactive} from "vue";

import { useStore } from "vuex";
import { getServices, getPlans } from "../services/addons"
import { calcCost } from "../services/charge"
import { ElMessageBox } from 'element-plus'

let id = 0

export default {
    name: "Pricing",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
    },
    setup() {
        const store = useStore()
        const state = reactive({
            clusters: ref(store.getters.clusters.map(item => {
                return {
                    value: item.uuid,
                    label: item.name,
                }
            })),
            activeName: 'overview',
            calculator: {
                cpu: 100,
                memory: 128,
                volume: 128,
                network: 10,
                resources: ['',],
                clusterID: ref(store.getters.currentCluster.uuid),
                total: 0,
            },
            props: {
                lazy: true,
                lazyLoad(node, resolve) {
                    const { level, value } = node
                    if(level == 0) {
                        getServices(state.calculator.clusterID).then(res=>{
                            if(res.data) {
                                const nodes = res.data.results.map((item) => ({
                                    value: item.name,
                                    label: item.name,
                                    leaf: false,
                                }))
                                resolve(nodes)
                            }
                        })
                    }else{
                        getPlans(state.calculator.clusterID, value).then(res=>{
                            if(res.data) {
                                const nodes = res.data.results.map((item) => ({
                                    value: item.name,
                                    label: item.name,
                                    description: item.description,
                                    leaf: true,
                                }))
                                resolve(nodes)
                            }
                        })
                    }
                },
            },
        })

        const openTips = (description) => {
            ElMessageBox.alert(description, '', {showClose: false})
        }

        const calculate = async () => {
            let data = [
                {
                    type: "cpu",
                    unit: "milli",
                    usage: state.calculator.cpu,
                    cluster_id: state.calculator.clusterID,
                },
                {
                    type: "memory",
                    unit: "bytes",
                    usage: state.calculator.memory * Math.pow(1024, 2),
                    cluster_id: state.calculator.clusterID,
                },
                {
                    type: "volume",
                    unit: "bytes",
                    usage: state.calculator.volume * Math.pow(1024, 2),
                    cluster_id: state.calculator.clusterID,
                },
                {
                    type: "network",
                    unit: "bytes",
                    usage: state.calculator.network * Math.pow(1024, 2),
                    cluster_id: state.calculator.clusterID,
                }
            ]
            for(let index in state.calculator.resources){
                let resource = state.calculator.resources[index]
                if(resource !== ''){
                    data.push({
                        type: `${resource[0]}:${resource[1]}`,
                        unit: "number",
                        usage: 1,
                        cluster_id: state.calculator.clusterID,
                    }) 
                }
            }
            console.log("cost request:", data)
            let res = await calcCost(data)
            if(res.data) {
                state.calculator.total = res.data.total
                console.log("cost response:", res.data)
            }
        }

        const addOneResource = async () => {
            state.calculator.resources.push('')
        }
        const removeOneResource = async (index) => {
            state.calculator.resources.splice(index, 1);
        }

        return {
            ...toRefs(state),
            openTips,
            calculate,
            addOneResource,
            removeOneResource,
        }

    }
}
