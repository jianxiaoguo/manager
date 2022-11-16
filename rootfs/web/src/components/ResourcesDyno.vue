<template>
    <div class="limit-width ember-view">
        <div class="group-header u-padding-Txs u-padding-Bxxs">
            <h5>Dynos</h5>
        </div>

        <div class="mv3 ember-view" v-if="processes.length<1">
            <div class="hk-well ember-view">
                <div class="f3 dark-gray lh-title mv1 ember-view">This app has no process types yet</div>
                Add a Procfile to your app in order to define its process types.
                <a href="https://www.drycc.cc/applications/managing-app-processes/" class="hk-link" target="_blank">Learn more</a>
            </div>
        </div>

        <div class="mb2 bg-white br1 shadow-outer-1 hk-hide-bb-last-row" role="list" v-if="processes.length>0">
            <div class="bb b--silver ph2 pv1 flex items-center " role="listitem" v-for="proc in processes" :key="proc.name">
                <div class="pa1">
                    <icon-terminal size="2.5rem" fill="#409EFF" class="dib br1 mr1 flex-shrink-0 self-start ember-view" />
                </div>

                <div class="mr4 flex dark-gray w-100 w-25-ns">
                    <div class="truncate">
                        <div class="ember-view">
                            <div class="purple no-underline link dib pv1 hk-focus-ring b">
                                {{proc.name}}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="nudge-up--1 ml3 dn dib-ns flex-auto">
                    <div class="ember-view">
                        <ul class="f6 pa0 ma0 attachments-dropdown">
                            <div class="btn-group ember-view">
                            </div>
                        </ul>
                    </div>
                </div>
                <div class="dark-gray f5 dn dib-ns mr2 truncate"></div>
                <div class="dark-gray f5 dn dib-ns mr2 truncate"><span>{{proc.cmd}}</span></div>
                <div class="dark-gray f5 dn dib-ns mr2 truncate w5 tr">
                    <span class="f5 text-uppercase light-green" v-if="proc.replicas > 0">{{proc.replicas}}D</span>
                    <span class="f5 text-uppercase light-red" v-if="proc.replicas < 1">{{proc.replicas}}D</span>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import ResourcesDyno from "./ResourcesDyno"
export default ResourcesDyno
</script>

<style scoped>

</style>
