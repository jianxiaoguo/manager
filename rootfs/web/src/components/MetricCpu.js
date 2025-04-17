import { reactive, computed, toRefs} from 'vue'


export default {
    name: "MetricCpu",
    props: {
        metricCpus: String
    },
    setup(props) {
        const factor = 1000 // MCORE
        const parsedCpus = computed(() => {
            try {
                return props.metricCpus ? JSON.parse(props.metricCpus) : {}
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
                            return value.toFixed(2) + ' ' + 'MCORE'
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
                const data = parsedCpus.value
                if (!data || Object.keys(data).length === 0) {
                    return []
                }
                return Object.entries(data).map(([name, points]) => ({
                    name,
                    data: points.map(([timestamp, value]) => [timestamp * 1000, ((typeof value === 'string' ? parseFloat(value) : value) * factor).toFixed(2)])
                }))
            }),
            minCpus: computed(() => {
                const metrics = parsedCpus.value
                if (!metrics || Object.keys(metrics).length === 0) return 0
                const values = Object.values(metrics).flat().map(item => Number(item[1]))
                return Math.ceil(Math.min(...values) * factor)
            }),
            maxCpus: computed(() => {
                const metrics = parsedCpus.value
                if (!metrics || Object.keys(metrics).length === 0) return 0
                const values = Object.values(metrics).flat().map(item => Number(item[1]))
                return Math.ceil(Math.max(...values) * factor)
            }),
            avgCpus: computed(() => {
                const metrics = parsedCpus.value
                if (!metrics || Object.keys(metrics).length === 0) return 0
                const values = Object.values(metrics).flat().map(item => Number(item[1]))
                return Math.ceil(values.reduce((sum, value) => sum + value, 0) / values.length * factor)
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
            hideOrShowChart,
        }
    }
}
