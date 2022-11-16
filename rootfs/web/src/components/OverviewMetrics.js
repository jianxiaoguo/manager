import { useRoute, useRouter } from 'vue-router'
import { reactive, toRefs, onMounted} from 'vue'
import {getResponseTimeMetrics, getThroughputMetrics, getMemoryMetrics} from "../services/metric";

export default {
    name: "OverviewMetrics",
    props: {
        appDetail: [Object, Function]
    },
    setup(props) {
        const router = useRouter()
        const options = {
            chart: {
                id: '',
                toolbar: {
                    show: false
                },
                tooltip: {
                    enabled: true
                }
            },
            xaxis: {
                type: 'datetime',
                labels: {
                    show: false,
                    // datetimeUTC: false,
                },
                axisTicks: {
                    show: false
                },
                tooltip: {
                    enabled: false
                },
                axisBorder: {
                    // show: false
                },
                // position: 'bottom',
            },
            grid: {
                show: false
            },
            yaxis: {
                show: false,
                tooltip: {
                    enable: false
                }
            },
            stroke: {
                curve: 'stepline',
                width: 1
            },
            tooltip: {
                enabled: false,
                y: {
                    formatter: function (val) {return val }
                },
                x: {
                    format: 'dd MMM HH:mm:ss'
                }
            }
        }

        const state = reactive({
            responseTimeOptions: JSON.parse(JSON.stringify(options)),
            responseTimeSeries: [{name: 'response time', data:[]}],
            memoryOptions: JSON.parse(JSON.stringify(options)),
            memorySeries: [{name: 'memory', data:[]}],
            throughputOptions: JSON.parse(JSON.stringify(options)),
            throughputSeries: [{name: 'throughput', data:[]}],
            latestResponseTime: 0,
            latestThroughput: 0,
            latestMemory: 0
        })

        state.responseTimeOptions.chart.id = 'response-time-metrics'
        state.responseTimeOptions.tooltip.y.formatter = function (val) {return val + ' ms'}

        state.throughputOptions.chart.id = 'throughput-metrics'
        state.throughputOptions.tooltip.y.formatter = function (val) {return val + ' rps'}

        state.memoryOptions.chart.id = 'memory-metrics'
        state.memoryOptions.tooltip.y.formatter = function (val) {return val + ' %'}

        const goToMetrics = () => {
            router.push({ path: `/apps/${props.appDetail.id}/metrics` })
        }

        onMounted(
            async () => {
                const m =  await getResponseTimeMetrics()
                if (!m) {
                    return
                }
                const data = m.map(item => {
                    return [item.time, item.duration]
                })
                state.latestResponseTime = data[data.length-1][1]
                state.responseTimeSeries = [{
                    name: 'response time',
                    data: data
                }]

                const m2 =  await getThroughputMetrics()
                if (!m2) {
                    return
                }

                const data2 = m2.map(item => {
                    return [item.time, item.num]
                })
                state.latestThroughput = data2[data2.length-1][1]
                state.throughputSeries = [
                    {
                        name: 'throughput',
                        data: data2
                    }
                ]

                const m3 =  await getMemoryMetrics()
                if (!m3) {
                    return
                }

                const data3 = m3.map(item => {
                    return [item.time, item.percentile]
                })
                state.latestMemory = data3[data3.length-1][1]
                state.memorySeries = [
                    {
                        name: 'memory',
                        data: data3
                    }
                ]

            },

        )

        return {
            ...toRefs(state),
            goToMetrics
        }

    }
}
