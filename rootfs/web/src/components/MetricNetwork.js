import { reactive, toRefs, computed, onMounted} from 'vue'

export default {
    name: "MetricNetwork",
    props: {
        metricNetworks: String
    },
    setup(props) {
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
                            return Math.ceil(value / 1024) + ' ' + 'KB'
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
            latest: computed(() => {
                try{
                    if(props.metricNetworks === ""){
                        return 0
                    }
                    length = JSON.parse(props.metricNetworks)[0].data.length
                    return Math.ceil(JSON.parse(props.metricNetworks)[0].data[length-1][1] / 1024)
                }catch(e){
                    return 0
                }
            }),
            max: computed(() => {
                try{
                    if(props.metricNetworks === ""){
                        return 0
                    }
                    var max = 0
                    JSON.parse(props.metricNetworks)[0].data.reduce(function(preItem, item){
                        if(max < preItem[1]){
                            max = preItem[1]
                        }
                        return item
                    })
                    return Math.ceil(max / 1024)
                }catch(e){
                    return 0
                }
            }),
            average: computed(() => {
                try{
                    if(props.metricNetworks === ""){
                        return 0
                    }
                    length = JSON.parse(props.metricNetworks)[0].data.length
                    var total = 0
                    JSON.parse(props.metricNetworks)[0].data.reduce(function(preItem, item){
                        total += preItem[1]
                        return item
                    })
                    return Math.ceil(total / (1024 * length))
                }catch(e){
                    return 0
                }
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

        onMounted(async () => {
            //
        })

        return {
            ...toRefs(state),
            hideOrShowChart
        }
    }
}
