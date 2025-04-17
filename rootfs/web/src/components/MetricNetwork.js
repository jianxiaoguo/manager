import { reactive, toRefs, computed, onMounted} from 'vue'

export default {
    name: "MetricNetwork",
    props: {
        title: String,
        metricNetworks: String
    },
    setup(props) {
        const factor = 1024 // KiB
        const parsedNetworks = computed(() => {
            try {
                return props.metricNetworks ? 
                    (typeof props.metricNetworks === 'string' 
                        ? JSON.parse(props.metricNetworks) 
                        : props.metricNetworks) 
                    : {}
            } catch {
                return {}
            }
        })
        const state = reactive({
            title: props.title,
            options: {
                noData: {
                    text: 'Loading...'
                },
                chart: {
                    id: 'metric-response-time',
                    tooltip: {
                        enabled: true
                    },
                    toolbar: {
                        show: false
                    }
                },
                xaxis: {
                    type: 'datetime',
                    labels: {
                        // show: false,
                        datetimeUTC: false,
                    },
                    tooltip: {
                        enabled: false
                    },
                    position: 'bottom',
                },
                yaxis: {
                    tickAmount: 4,
                    labels: {
                        formatter: (value) => {
                            return value.toFixed(2) + ' ' + 'KiB'
                        }
                    }
                },
                stroke: {
                    curve: 'stepline',
                    width: 1
                },
                tooltip: {
                    x: {
                        format: 'dd MMM HH:mm:ss'
                    }
                },
            },
            //series: props.metricNetworks ? props.metricNetworks : [],
            series : computed(() => {
                const data = parsedNetworks.value
                if (!data || Object.keys(data).length === 0) {
                    return []
                }
                return Object.entries(data).map(([podName, points]) => ({
                    name: podName,
                    data: points.map(([timestamp, value]) => ({
                        x: timestamp * 1000, // 转换为毫秒
                        y: ((typeof value === 'string' ? parseFloat(value) : value) / factor).toFixed(2)
                    }))
                }))
            }),
            minNets: computed(() => {
                const metrics = parsedNetworks.value
                if (!metrics || Object.keys(metrics).length === 0) return "0.00"
                const values = Object.values(metrics).flat().map(item => typeof item[1] === 'string' ? parseFloat(item[1]) : item[1])
                return (Math.min(...values) / factor).toFixed(2)
            }),
            maxNets: computed(() => {
                const metrics = parsedNetworks.value
                if (!metrics || Object.keys(metrics).length === 0) return "0.00"
                const values = Object.values(metrics).flat().map(item => typeof item[1] === 'string' ? parseFloat(item[1]) : item[1])
                return (Math.max(...values) / factor).toFixed(2)
            }),
            avgNets: computed(() => {
                const metrics = parsedNetworks.value
                if (!metrics || Object.keys(metrics).length === 0) return "0.00"
                const values = Object.values(metrics).flat().map(item => typeof item[1] === 'string' ? parseFloat(item[1]) : item[1])
                return ((values.reduce((sum, value) => sum + value, 0) / values.length) / factor).toFixed(2)
            }),
            isHide: false,
            hideStyle: Object
        })

        const hideOrShowChart = () => {
            state.isHide = !state.isHide
            if (state.isHide) {
                state.hideStyle = {
                    top: '-9999px',
                    left: '-999px',
                    visibility: 'hidden'
                }
            } else {
                state.hideStyle = null
            }

        }
        return {
            ...toRefs(state),
            hideOrShowChart
        }
    }
}
