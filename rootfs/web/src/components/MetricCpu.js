import { reactive, computed, toRefs} from 'vue'


export default {
    name: "MetricCpu",
    props: {
        metricCpus: String
    },
    setup(props) {
        const factor = 1
        const cpuList = []
        JSON.parse(props.metricCpus)[0].data.forEach(item => {cpuList[cpuList.length] = Math.ceil(item[1] / factor)})
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
                            return Math.ceil(value / factor) + ' ' + 'NCORE'
                        }
                    }

                },
                stroke: {
                    curve: 'stepline',
                    width: 1
                },
                tooltip: {
                    y: {
                        formatter: function (val) {
                            return Math.ceil(val / factor)
                        }
                    },
                    x: {
                        format: 'dd MMM HH:mm:ss'
                    }
                },
            },
            series : computed(() => {
                if(props.metricCpus === ""){
                    return []
                }
                return JSON.parse(props.metricCpus)
            }),
            minCpus: computed(() => cpuList.length > 0 ? Math.min.apply(Math, cpuList) : 0),
            maxCpus: computed(() => cpuList.length > 0 ? Math.max.apply(Math, cpuList) : 0),
            avgCpus: computed(() => Math.ceil(cpuList.reduce((total, current) => total + current) / cpuList.length)),
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
