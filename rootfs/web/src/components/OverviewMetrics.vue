<template>
    <div class="app-overview-metrics">
        <div class="ember-view">
            <div class="flex-ns items-center pv2">
                <div class="flex dark-gray mr2">Metrics (last 24hrs)</div>
                <div class="flex-auto"></div>
                <a @click="goToMetrics" class="flex items-center hk-link no-underline f6 mv1 mv0-ns ember-view">
                    <span class="underline">All Metrics</span>
                    <icon-arrow-circle-right class="ml--3 nudge-down--1" size="1.2rem"/>
                </a>
            </div>

            <div class="metrics__summary-row metrics__summary-row--favorite items-end ember-view">
                <div class="w-100 metrics__summary-container" >
                    <a @click="goToMetrics" class="ember-view link metrics__summary-row--favorite__link-wrapper anim-fade-in">

                        <div title="Your latest 95th percentile response time" class="metrics__summary-row__item metrics__wrapped-chart b--black-05 flex-column ember-view">
                            <div class="metrics__summary-row__label">
                                response time
                            </div>
                            <div class="metric-wrapper flex items-end">
                                <div class="metrics__summary-row__value metrics__summary-row__value--large">
                                    {{latestResponseTime}}
                                    <span class="metrics__summary-row__unit">ms</span>
                                </div>
                                <div class="flex-grow-1" title="Response time over past 24hrs">
                                    <apexchart height="60" type="line" :options="responseTimeOptions" :series="responseTimeSeries"></apexchart>
                                </div>
                            </div>
                        </div>

                        <div title="Latest web requests per second" class="metrics__summary-row__item metrics__wrapped-chart b--black-05 flex-column ember-view">
                            <div class="metrics__summary-row__label">
                                throughput
                            </div>
                            <div class="metric-wrapper flex items-end">
                                <div class="metrics__summary-row__value metrics__summary-row__value--large">
                                    {{latestThroughput}}
                                    <span class="metrics__summary-row__unit">rps</span>
                                </div>
                                <div class="flex-grow-1" title="Throughput over past 24hrs">
                                    <apexchart height="60" type="line" :options="throughputOptions" :series="throughputSeries"></apexchart>
                                </div>
                            </div>
                        </div>

                        <div title="Latest memory usage" class="metrics__summary-row__item metrics__wrapped-chart b--black-05 flex-column ember-view">
                            <div class="metrics__summary-row__label">
                                memory
                            </div>
                            <div class="metric-wrapper flex items-end">
                                <div class="metrics__summary-row__value metrics__summary-row__value--large">
                                    {{latestMemory}}
                                    <span class="metrics__summary-row__unit">%</span>
                                </div>
                                <div class="flex-grow-1" title="Memory Usage over past 24hrs">
                                    <apexchart height="60" type="line" :options="memoryOptions" :series="memorySeries"></apexchart>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import OverviewMetrics from "./OverviewMetrics"
export default OverviewMetrics
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
</style>
