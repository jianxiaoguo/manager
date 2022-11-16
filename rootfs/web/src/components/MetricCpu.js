import { reactive, computed, toRefs} from 'vue'


export default {
    name: "MetricCpu",
    props: {
        metricCpus: String
    },
    setup(props) {
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
                            return Math.ceil(value / 1000) + ' ' + 'MCORE'
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
                            return Math.ceil(val / 1000)
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
            latestCpus: computed(() => {
                try{
                    if(props.metricCpus === ""){
                        return 0
                    }
                    length = JSON.parse(props.metricCpus)[0].data.length
                    var latestMem = Math.ceil(JSON.parse(props.metricCpus)[0].data[length-1][1] / 1024)
                    var count = 0
                    JSON.parse(props.metricCpus)[0].data.reduce(function(preItem, item){
                        if(Math.ceil(preItem[1] / 1024) == latestMem){
                            count += 1
                        }
                        return item
                    })
                    state.latestPercent = Math.ceil((count / length) * 100)
                    return latestMem
                }catch(e){
                    return 0
                }
            }),
            latestPercent: 0,
            maxCpus:  computed(() => {
                try{
                    if(props.metricCpus === ""){
                        return 0
                    }

                    var max = 0
                    JSON.parse(props.metricCpus)[0].data.reduce(function(preItem, item){
                        if(max < preItem[1]){
                            max = preItem[1]
                        }
                        return item
                    })
                    var maxMem = Math.ceil(max / 1024)

                    length = JSON.parse(props.metricCpus)[0].data.length
                    var count = 0
                    JSON.parse(props.metricCpus)[0].data.reduce(function(preItem, item){
                        if(Math.ceil(preItem[1] / 1024) == maxMem){
                            count += 1
                        }
                        return item
                    })
                    state.maxPercent = Math.ceil((count / length) * 100)

                    return maxMem
                }catch(e){
                    return 0
                }
            }),
            maxPercent: 0,
            avgCpus: computed(() => {
                try{
                    if(props.metricCpus === ""){
                        return 0
                    }
                    length = JSON.parse(props.metricCpus)[0].data.length
                    var total = 0
                    JSON.parse(props.metricCpus)[0].data.reduce(function(preItem, item){
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

        return {
            ...toRefs(state),
            hideOrShowChart,
        }
    }
}
