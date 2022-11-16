<template>
    <div class="add-ons ember-view">
        <div class="flex-ns items-center pv2">
            <div class="flex dark-gray mr2">
                <div class="mr1">Installed add-ons</div>
            </div>
            <div class="flex-auto"></div>

            <a @click="goToResources" class="flex items-center hk-link no-underline f6 mv1 mv0-ns ember-view">
                <span class="underline">Details Add-ons</span>
                <icon-arrow-circle-right class="ml--3 nudge-down--1" size="1.2rem"/>
            </a>
        </div>

        <ul class="addons-grid list pl0 flex mb5 bg-lightest-silver shadow-outer-1 br1 overflow-hidden" v-if="addons.length > 0">
            <li class="addon ph3 pv2 flex b--silver bg-white" v-for="addon in addons" :key="addon.name">
                <a href="" class="mt1" target="_blank" rel="noopener noreferrer">
                    <div class="relative">
                        <icon-components size="2.5rem" fill="#409EFF" class="icon malibu-icon malibu-fill-gradient-purple nudge-left--2 nudge-up--1" />
                    </div>
                </a>
                <div class="ember-view ma0 pl2 flex-auto-l">
                    <div>
                        <div class="fl">
                            <div>
                                <span class="hk-link purple no-underline ">
                                    {{addon.plan}}               
                                </span>
                            </div>
                            <div>
                                <span class="f5 gray nudge-up-1">
                                    {{addon.name}}
                                </span>
                            </div>
                        </div>
                        <div class="fr mt2">
                            <span class="f5 gray nudge-up-1 light-green" v-if="addon.status === 'Ready'">{{addon.status}}</span>
                            <span class="f5 gray nudge-up-1 light-red" v-else>{{addon.status}}</span>
                        </div>
                    </div>
                </div>
            </li>
        </ul>


        <div class="mb5 ember-view" v-if="addons.length === 0">
            <div class="hk-well ember-view">
                <div class="f3 dark-gray lh-title mv1 ember-view">
                    There are no add-ons for this app
                </div>
                <div class="f5 gray lh-copy ember-view">
                    You can add add-ons to this app and they will show here.
                    <a href="https://www.drycc.cc/applications/managing-app-resources" class="hk-link" target="_blank">Learn more</a>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import OverviewAddons from "./OverviewAddons"
export default OverviewAddons
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
</style>
