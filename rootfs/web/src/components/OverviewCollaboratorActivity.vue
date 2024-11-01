<template>
    <div class="ember-view">
        <div class="dib w-100 flex-ns items-center pv2">
            <div class="flex dark-gray mr2">
                <div class="mr1">Latest collaborator (last 30 activities)</div>
            </div>

            <div class="flex-auto"></div>

            <a @click="goToAccess" class="flex items-center hk-link no-underline f6 mv1 mv0-ns ember-view">
                <span class="underline">Manage Access</span>
                <icon-arrow-circle-right class="ml--3 nudge-down--1" size="1.2rem"/>
            </a>
        </div>
        <div class="bule-box">
            <div class="ph3 pv1">
                <div class="collaborator f5 ember-view">
                    <div class="mv2 flex items-center" v-for="ca in activities" :key="ca.username">
                        <div class="avatar mr2">
                            <span style="width:28px; height:28px" class="gravatar-icon br-100 ember-view" >
                                <img :src="'/v1/avatar/' + ca.username" />
                            </span>
                        </div>
                        <div class="user-info">{{ca.username}}</div>
                        <div class="flex-auto"></div>

                        <div class="flex items-center">
                            <svg style="height: 16px; width: 16px;" class="icon malibu-icon malibu-fill-gradient-gray nudge-up--1 mr1" >
                                <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#deploy-16"></use>
                            </svg>
                            <div class="b mr1">{{ca.count}} </div>deploys
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import OverviewCollaboratorActivity from "./OverviewCollaboratorActivity"
export default OverviewCollaboratorActivity
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
</style>
