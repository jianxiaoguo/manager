import { reactive, computed, toRefs} from 'vue'

export default {
    name: "MetricMemory",
    props: {
        metricMemory: String,
    },
    setup(props) {
        const factor = 1024
        const memList = []
        JSON.parse(props.metricMemory)[0].data.forEach(item => {memList[memList.length] = Math.ceil(item[1] / factor)})
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
                            return Math.ceil(value / factor) + ' ' + 'KiB'
                        }
                    }
                },
                stroke: {
                    curve: 'stepline',
                    width: 1
                },
                tooltip: {
                    y: {
                        formatter: function (val) {return Math.ceil(val / factor) }
                    },
                    x: {
                        format: 'dd MMM HH:mm:ss'
                    }
                },
            },
            series : computed(() => {
                if(props.metricMemory === ""){
                    return []
                }
                return JSON.parse(props.metricMemory)
            }),
            minMem: computed(() => memList.length > 0 ? Math.min.apply(Math, memList) : 0),
            maxMem: computed(() => memList.length > 0 ? Math.max.apply(Math, memList) : 0),
            avgMem: computed(() => Math.ceil(memList.reduce((total, current) => total + current) / memList.length)),
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
