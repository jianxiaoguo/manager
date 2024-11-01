import { reactive, toRefs, computed, onMounted} from 'vue'

export default {
    name: "MetricNetwork",
    props: {
        metricNetworks: String
    },
    setup(props) {
        const factor = 1024
        const netList = []
        JSON.parse(props.metricNetworks)[0].data.forEach(item => {netList[netList.length] = Math.ceil(item[1] / factor)})
        const state = reactive({
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
                    // tickAmount: 4,
                    labels: {
                        formatter: (value) => {
                            return Math.ceil(value / 1024) + ' ' + 'KiB'
                        }
                    }

                },
                stroke: {
                    curve: 'stepline',
                    width: 1
                },
                tooltip: {
                    y: {
                        formatter: function (val) {return Math.ceil(val / 1024) }
                    },
                    x: {
                        format: 'dd MMM HH:mm:ss'
                    }
                },
            },
            //series: props.metricNetworks ? props.metricNetworks : [],
            series : computed(() => {
                if(props.metricNetworks === ""){
                    return []
                }
                return JSON.parse(props.metricNetworks)
            }),
            minNets: computed(() => netList.length > 0 ? Math.min.apply(Math, netList) : 0),
            maxNets: computed(() => netList.length > 0 ? Math.max.apply(Math, netList) : 0),
            avgNets: computed(() => Math.ceil(netList.reduce((total, current) => total + current) / netList.length)),
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

        onMounted(async () => {
            //
        })

        return {
            ...toRefs(state),
            hideOrShowChart
        }
    }
}
