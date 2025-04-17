<template>
    <div class="sortable-item ember-view">
        <div class="metrics__wrapped-chart b--black-05 flex-column bb ember-view">
            <div class="metrics__chart w-100 ember-view">
                <div class="w-100">
                    <header class="metrics__chart__header ember-view">
                        <div class="flex flex-auto items-center flex-wrap items-start pl3 pv3 f5">
                            <button @click="hideOrShowChart" class="bg-transparent hk-focus-ring--blue:focus cursor-hand br1 ba0 b--none pa--1" title="Hide event metrics" type="button" >
                                <span class="clip">Hide event metrics</span>
                                <svg :class="{'rot90': !isHide}" style="height: 16px; width: 16px;" class="icon malibu-icon  mr1 pointer nudge-up--2" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4935" width="16" height="16"><path d="M333.1 118.9l-35.3 35.4L655.5 512 297.8 869.7l35.3 35.4L726.2 512z" fill="" p-id="4936"></path></svg>
                            </button>

                            <div class="flex flex-row">
                                <div class="f5 b dark-gray pointer ">{{title}}</div>
                                <span title="" class="ml1 tooltip-component ember-view">
                                    <svg style="height: 14px; width: 14px;" class="icon malibu-icon metrics__chart__devcenter-link malibu-fill-gradient-dark-gray pointer nudge-right--1" data-test-icon-name="info-badge-16" data-test-target="malibu-icon" aria-hidden="true" role="img">
                                <!---->  <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#info-badge-16"></use>
                                    </svg>
                                </span>
                            </div>
                        </div>

                        <div class="ember-view">
                            <div class="metrics__summary-row">
                                <div class="metrics__summary-row__item ember-view">
                                    <span title="" class="tooltip-component ember-view" >
                                        <div class="ph3">
                                            <div class="metrics__summary-row__label">MIN</div>
                                            <div class="metrics__summary-row__values">
                                                <div class="metrics__summary-row__value metrics__summary-row__value--default metrics__summary-row__value--primary metrics__summary-row__value">
                                                    {{minNets}}<span class="metrics__summary-row__unit">KiB</span>
                                                </div>

                                            </div>
                                        </div>
                                    </span>
                                </div>
                                <div class="metrics__summary-row__item ember-view">
                                    <span title="" class="tooltip-component ember-view" data-original-title="The maximum amount of memory used in this time period.">
                                        <div class="ph3">
                                            <div class="metrics__summary-row__label">MAX</div>
                                            <div class="metrics__summary-row__values">
                                                <div class="metrics__summary-row__value metrics__summary-row__value--default metrics__summary-row__value--primary metrics__summary-row__value">
                                                    {{maxNets}}<span class="metrics__summary-row__unit">KiB</span>
                                                </div>

                                            </div>
                                        </div>
                                    </span>
                                </div>
                                <div class="metrics__summary-row__item ember-view">
                                    <span title="" class="tooltip-component ember-view" data-original-title="The average amount of memory used in this time period.">
                                        <div class="ph3">
                                            <div class="metrics__summary-row__label">AVERAGE</div>
                                            <div class="metrics__summary-row__values">
                                                <div class="metrics__summary-row__value metrics__summary-row__value--default metrics__summary-row__value--primary metrics__summary-row__value">
                                                    {{avgNets}}<span class="metrics__summary-row__unit">KiB</span>
                                                </div>

                                            </div>
                                        </div>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </header>
                    <div class="w-100 flex metrics__chart__wrapper" :class="{'absolute': isHide}" :style="hideStyle">
                        <div class="flex flex-grow-1 metrics__chart__graphs">
                            <apexchart id="mem-chart" class="flex-grow-1 metrics__chart__image" height="170" type="line" :options="options" :series="series"></apexchart>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import MetricNetwork from "./MetricNetwork"
export default MetricNetwork
</script>

<style scoped>

</style>
