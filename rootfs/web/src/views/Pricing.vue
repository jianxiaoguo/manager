<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative mt5">
      <div class="main-content">
        <el-tabs v-model="activeName">
          <el-tab-pane label="Overview" name="overview"></el-tab-pane>
          <el-tab-pane label="Calculator" name="calculator"></el-tab-pane>
        </el-tabs>
        <ul v-if="activeName=='overview'" class="list-group list-group-lg">
          <li class="list-group-item ember-view">
            <div class="panel-section">
                <div class="section-description">
                    <div class="section-title f3 bule" role="heading" aria-level="3">
                        Drycc Basic Pricing
                    </div>
                    <div class="mt2 f5 lh-copy dark-gray">
                        Let pricing be like tap water. You can use as much as you want.
                    </div>
                </div>

                <div class="panel-content">
                    <h4>Ptypes</h4>
                    <p>Drycc runs your app in lightweight, isolated Linux containers called "ptypes". As a small start-up team, you can focus more on the business itself, you can view it this way.</p>
                    <pre>$ drycc ps:list -a yourapp </pre>
                    <h4>Resources</h4>
                    <p>Drycc different from other cloud computing vendors, drycc's CPU, memory and volume can be customized, like this.</p>
                    <pre>$ drycc limits:set --cpu web=500m --memory web=2G -a yourapp </pre>
                    
                    <h4>Billing Cycle</h4>
                    <p>Every hour is regarded as a billing cycle, and less than one hour is calculated as one hour.Such billing rules can make your business more flexible and flexible; Help you save more costs, autoscale like this.</p>
                    <pre>$ drycc autoscale:set  web --min=3 --max=20 --cpu-percent=50 </pre>
                </div>
            </div>
          </li>
          <li class="list-group-item ember-view">
            <div class="panel-section">
                <div class="section-description">
                    <div class="section-title f3 bule" role="heading" aria-level="3">
                        Drycc Resource Pricing
                    </div>
                    <div class="mt2 f5 lh-copy dark-gray">
                        Tools and services for developing, extending, and operating your app.
                    </div>
                </div>

                <div class="panel-content">
                    <h4>Overview</h4>
                    <p>Drycc resources are components that support your application, such as data storage, monitoring, analytics, data processing, and more. </p>
                    <pre>$ drycc resources --help </pre>
                    <h4>Resource Install</h4>
                    <p>Resources are installed onto applications by using the drycc. Most resources offer multiple plans, with different features, capabilities, and prices.</p>
                    <pre>$ drycc resources:create mysql:plan-250 -a yourapp </pre>
                    
                    <h4>Why Use Resources</h4>
                    <p>
                      Resources exist so that developers can focus on their own application logic,
                      and not the additional complexity of keeping supporting services running at full production capacity, 
                      <a href="https://www.drycc.cc/applications/managing-app-resources/" class="hk-link nowrap">learn more</a>.
                    </p>
                </div>
            </div>
          </li>
        </ul>
        <ul v-else class="list-group list-group-lg">
          <el-form ref="form" :model="calculator" label-width="120px">
            <li class="list-group-item ember-view">
              <div class="panel-section">
                  <div class="section-description">
                      <div class="section-title f3 bule" role="heading" aria-level="3">
                          Price Calculator
                      </div>
                      <div class="mt2 f5 lh-copy dark-gray">
                          Enter your resource requirements to help you calculate the cost, the results are for reference only.
                      </div>
                  </div>          
                  <div class="panel-content">
                      <h4>Cluster Zone</h4>
                      <p>Please select the cluster closest to the business to obtain the best user experience.</p>
                      <div class="hk-well ember-view text-left u-padding-As mt1">
                        <el-select v-model="calculator.clusterID" class="m-2" placeholder="Select Zone" style="width: 16rem;">
                          <el-option
                            v-for="cluster in clusters"
                            :key="cluster.value"
                            :label="cluster.label"
                            :value="cluster.value"
                          >
                          </el-option>
                        </el-select>
                      </div>
                      <h4>CPU</h4>
                      <p>The charging unit of CPU is milli, abbreviation M, 1000M CPU = 1 CPU.</p>
                      <pre><el-input-number v-model="calculator.cpu" style="width: 16rem;"></el-input-number><div class="pull-right mt1">Milli</div></pre>
                      <h4>Memory</h4>
                      <p>The charging unit of memory is megabyte, abbreviation MB.</p>
                      <pre><el-input-number v-model="calculator.memory" style="width: 16rem;"></el-input-number><div class="pull-right mt1">Megabyte</div></pre>
                      <h4>Volume</h4>
                      <p>The charging unit of volume is megabyte, abbreviation MB.</p>
                      <pre><el-input-number v-model="calculator.volume" style="width: 16rem;"></el-input-number><div class="pull-right mt1">Megabyte</div></pre>
                      <h4>Network</h4>
                      <p>Network is billed according to traffic, the charging unit is Megabyte, abbreviation MB.</p>
                      <pre><el-input-number v-model="calculator.network" style="width: 16rem;"></el-input-number><div class="pull-right mt1">Megabyte/Hour</div></pre>
                      <h4><div class="mr1 pull-left"><icon-add size="1.2rem" fill="#67C23A" @click="addOneResource()"/></div>Resources</h4>
                      <p>Please add the resources and plans you need to use.</p>
                      <div class="hk-well ember-view text-left u-padding-As mt1" v-for="(_, index) in calculator.resources" :key="index">
                        <el-cascader :disabled="calculator.clusterID == ''" :props="props" v-model="calculator.resources[index]" style="width: 16rem;">
                          <template #default="{ node, data }">
                            <div v-if="node.isLeaf" v-bind:title="data.description">
                              <span>{{ data.label }}</span>
                              <icon-tips class="pull-right" size="1.2rem" fill="#67C23A" @click="openTips(data.description)"></icon-tips>
                            </div>
                            <div v-else>
                              <span>{{ data.label }}</span>
                            </div>
                          </template>
                        </el-cascader>
                        
                        <div class="pull-right mt1">Plan/Hour</div>
                        <div class="mt1 mr3 pull-right">
                          <icon-reduce size="1.2rem" fill="#F56C6C" @click="removeOneResource(index)"/>
                        </div>
                      </div>
                  </div>
              </div>
            </li>
             <li class="list-group-item ember-view">
              <div class="panel-section">
                  <div class="section-description">
                      <div class="section-title f3 bule" role="heading" aria-level="3">
                          Total
                      </div>
                  </div>          
                  <div class="panel-content">
                    <div class="pull-right">{{this.$toPrice(calculator.total)}}/Hour</div>
                  </div>
                  <div class="panel-content">
                    <div class="pull-right">No Tax</div>
                  </div>
              </div>
             </li>
            <li class="list-group-item ember-view">
              <div class="panel-section">
                  <div class="section-description">
                  </div>          
                  <div class="panel-content">
                    <div class="pull-right"><el-button type="success" @click="calculate">calculate</el-button></div>
                  </div>
              </div>
             </li>
          </el-form>
        </ul>
      </div>
  </div>
  <main-footer />
</div>
</template>

<script>
import Pricing from "./Pricing"
export default Pricing
</script>

<style scoped>

</style>
