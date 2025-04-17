import { reactive, computed, toRefs} from 'vue'

export default {
    name: "MetricMemory",
    props: {
        metricMemory: String,
    },
    setup(props) {
        const factor = 1024 * 1024 // MiB
        const parsedMemory = computed(() => {
            try {
                return props.metricMemory ? JSON.parse(props.metricMemory) : {}
            } catch {
                return {}
            }
        })
        const state = reactive({
            options: {
                noData: {
                    text: 'Loading...'
                },
                chart: {
                    id: 'metric-mem',
                    events: {
                        zoomed: function(chartContext, a ) {
                            console.log(a)
                        }
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
                            return value.toFixed(2) + ' ' + 'MiB'
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
            series : computed(() => {
                const data = parsedMemory.value
                if (!data || Object.keys(data).length === 0) {
                    return []
                }
                return Object.entries(data).map(([name, points]) => ({
                    name,
                    data: points.map(([timestamp, value]) => [timestamp * 1000, ((typeof value === 'string' ? parseFloat(value) : value) / factor).toFixed(2)])
                }))
            }),
            minMem: computed(() => {
                const metrics = parsedMemory.value
                if (!metrics || Object.keys(metrics).length === 0) return "0.00"
                const values = Object.values(metrics).flat().map(item => (typeof item[1] === 'string' ? parseFloat(item[1]) : item[1]) / factor)
                return Math.min(...values).toFixed(2)
            }),
            maxMem: computed(() => {
                const metrics = parsedMemory.value
                if (!metrics || Object.keys(metrics).length === 0) return "0.00"
                const values = Object.values(metrics).flat().map(item => (typeof item[1] === 'string' ? parseFloat(item[1]) : item[1]) / factor)
                return Math.max(...values).toFixed(2)
            }),
            avgMem: computed(() => {
                const metrics = parsedMemory.value
                if (!metrics || Object.keys(metrics).length === 0) return "0.00"
                const values = Object.values(metrics).flat().map(item => (typeof item[1] === 'string' ? parseFloat(item[1]) : item[1]) / factor)
                return (values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(2)
            }),
            avgPercent: 0,
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
            hideOrShowChart,
        }
    }
}
