<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box>
            <template v-slot:nav-cluster>
                <cluster-app-detail :app-detail="appDetail"/>
            </template>
            <template v-slot:navbox-extension>
                <nav-box-app-detail-menu :app-detail="appDetail"/>
            </template>
        </nav-box>
        <div class="main-content">
          <main-nav :is-metrics-active="true" :app-detail="appDetail"/>
          <div class="ember-view" v-if="processTypes.length <= 0">
            <div class="mb5 ember-view" style="padding: 0px 320px;">
              <div class="f3 dark-gray lh-title mv1 ember-view"> This app has no process types yet </div>
              <div class="f5 gray lh-copy ember-view">
                Add a Procfile to your app in order to define its process types.
                <a href="https://www.drycc.cc/applications/managing-app-processes/" class="hk-link" target="_blank">Learn more</a>
              </div>
            </div>
          </div>
          <div v-if="processTypes.length > 0">
            <div class="limit-width">
                <div class="flex flex-column metrics__charts-container">
                    <div id="process-picker" class="relative dib mb2">
                        <div class="pull-left" style="width: 384.36px;">
                            <el-select v-model="currentProcess" class="m-2" placeholder="Select">
                                <el-option
                                v-for="pt in processTypes"
                                :key="pt.name"
                                :label="pt.name"
                                :value="pt.name"
                                />
                            </el-select>
                        </div>
                        <div class="pull-right">
                            <el-radio-group v-model="interval">
                                <el-radio-button value="5">5 minute</el-radio-button>
                                <el-radio-button value="10">10 minute</el-radio-button>
                                <el-radio-button value="20">20 minute</el-radio-button>
                                <el-radio-button value="30">30 minute</el-radio-button>
                            </el-radio-group>
                        </div>
                    </div>
                    
                    <div class="bule-box mt2 mb4">
                        <div class="ember-view">
                            <div class="ember-view">
                                <div class="metrics__main__charts metrics__chart-sorting is-vertical">
                                    <metric-cpu :key="Math.random()" :metricCpus="metricCpus"/>
                                    <metric-memory :key="Math.random()" :metricMemory="metricMemory"/>
                                    <metric-network :key="Math.random()" :metricNetworks="metricReceiveNetworks" title="Network RX Usage"/>
                                    <metric-network :key="Math.random()" :metricNetworks="metricTransmitNetworks" title="Network TX Usage"/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AppDetailMetrics from  "./AppDetailMetrics"
export default AppDetailMetrics
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
    .hide-el {
        display: none;
    }
</style>
