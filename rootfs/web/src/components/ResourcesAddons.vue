<template>
    <div class="limit-width ember-view">
        <div class="group-header u-padding-Txs u-padding-Bxxs">
            <h5>Resources</h5>
        </div>

        <div class="mv3 ember-view" v-if="addons.length<1">
            <div class="hk-well ember-view">
                <div class="f3 dark-gray lh-title mv1 ember-view"> There are no resources for this app </div>
                <div class="f5 gray lh-copy ember-view"> You can add resources to this app and they will show here.
                    <a href="https://www.drycc.cc/applications/managing-app-resources/" class="hk-link" target="_blank">Learn more</a>
                </div>
            </div>
        </div>

        <div class="mb2 bg-white br1 shadow-outer-1 hk-hide-bb-last-row" role="list" v-if="addons.length>0">
            <div class="bb b--silver ph2 pv1 flex items-center " role="listitem" v-for="addon in addons" :key="addon.name">
                <div class="pa1">
                    <icon-components size="2.5rem" fill="#409EFF" class="dib br1 mr1 flex-shrink-0 self-start ember-view" />
                </div>

                <div class="mr4 flex dark-gray w-100 w-25-ns">
                    <div class="truncate">
                        <div class="ember-view">
                            <div class="purple no-underline link dib pv1 hk-focus-ring b">
                                {{addon.name}}
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
                <div class="dark-gray f5 dn dib-ns mr2 truncate"><span>{{addon.plan}}</span></div>
                <div class="dark-gray f5 dn dib-ns mr2 truncate w5 tr">
                    <span class="light-green" v-if="addon.status === 'Ready'">{{addon.status}}</span>
                    <span class="light-red" v-else>{{addon.status}}</span>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import ResourcesAddons from "./ResourcesAddons"
export default ResourcesAddons
</script>

<style scoped>

</style>
