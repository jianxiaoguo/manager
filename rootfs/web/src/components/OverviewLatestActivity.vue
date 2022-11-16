<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <div class="flex-ns items-center limit-width pv2">
        <div class="flex dark-gray mr2">Latest activity (last 15 activities)</div>
        <div class="flex-auto"></div>
        <a @click="goToActivity" class="flex items-center hk-link no-underline f6 mv1 mv0-ns ember-view">
            <span class="underline">All Activity</span>
             <icon-arrow-circle-right class="ml--3 nudge-down--1" size="1.2rem"/>
        </a>
    </div>

    <div class="hk-hide-bb-last-row list-group limit-width ember-view">
        <div class="flex bb pv3 b--light-silver activity-item ember-view" v-for="activity in activities" :key="activity.username">
            <div class="pt1 mr3 nowrap">
                <div class="relative dib ember-view">
                    <template v-if="activity.failed">
                        <icon-error size="2.5rem" class="icon malibu-icon fill-dark-gray" fill="#d00202" />
                    </template>
                    <template v-else>
                        <icon-success size="2.5rem" class="icon malibu-icon fill-dark-gray" />
                    </template>
                </div>
                <span style="width:28px; height:28px" class="mb1 ml2 gravatar-icon br-100 ember-view">
                    <img :src="'/v1/avatar/' + activity.username">
                </span>
            </div>
            <div class="flex flex-column lh-copy">
                <div class="f5">
                    <span class="b">{{activity.username}}:</span>
                    <span>{{activity.content}}</span>
                </div>
                <div class="f5 gray">
                    <span :title="activity.createdTime" class="timeago ember-view">{{activity.created_time}}</span>
                    ·
                    {{activity.version}}
                </div>
            </div>
        </div>

    </div>
</div>
</template>

<script>
import OverviewLatestActivity from "./OverviewLatestActivity"
export default OverviewLatestActivity
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
</style>
