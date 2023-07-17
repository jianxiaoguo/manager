<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <activity-roll-back v-if="isShowRollBack && rollBackIndex>0"
                        :activities="activities"
                        :rollBackIndex="rollBackIndex"
                        :appDetail="appDetail"
                        @closeRB="closeRollBack"
    />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box>
            <template v-slot:nav-cluster>
                <cluster-app-select :app-detail="appDetail"/>
            </template>
            <template v-slot:navbox-extension>
                <nav-box-app-detail-menu :app-detail="appDetail"/>
            </template>
        </nav-box>
        <div class="main-content">
            <main-nav :is-activity-active="true" :app-detail="appDetail"/>
            <h5 class="limit-width">Activity Feed</h5>
            <div class="hk-hide-bb-last-row list-group limit-width ember-view">
                <div class="flex bb pv3 b--light-silver activity-item ember-view" v-for="(activity, index) in activities">
                    <div class="pt1 mr3 nowrap">
                    <template v-if="activity.failed">
                        <icon-error size="2.5rem" class="icon malibu-icon fill-dark-gray" fill="#d00202" />
                    </template>
                    <template v-else>
                        <icon-success size="2.5rem" class="icon malibu-icon fill-dark-gray" />
                    </template>
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
<!--                            <span :title="activity.createdTime.format('yyyy.MM.dd hh:mm:ss')" class="timeago ember-view">{{activity.createdTime.format("yyyy-MM-dd at hh:mm")}}</span>-->
                            <span :title="activity.createdTime" class="timeago ember-view">{{activity.created_time}}</span>
                            ·
                            {{activity.version}}

                            <span class="confirmable-action ember-view" v-if="activity.version > 1">·
                                <a @click="openRollBack(activity.version)" href="#" class="hk-link rollback">
                                    Roll back to here
                                </a>
                            </span>
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
import AppDetailActivity from "./AppDetailActivity"
export default AppDetailActivity
</script>

<style scoped>

</style>
