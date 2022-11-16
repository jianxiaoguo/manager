<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
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
            <main-nav :is-deploy-active="true" :app-detail="appDetail"/>
            <div class="deploy-section">
                <ul class="list-group list-group-lg">
                    <li class="deploy-github list-group-item ember-view">
                        <div class="panel-section ">
                            <div class="section-description">
                                <div class="section-title f3 purple">Deployment method</div>
                            </div>
                            <div class="panel-content">
                                <ul class="nav deploy-nav nav-pills">
                                    <li class="deploy-tab tab-heroku-git">
                                        <a @click="goToDryccGit" href="#" class="ember-view" :class="{'active': depolyType==='drycc-git'}">
                                            <icon-branch size="2.5rem" class="icon malibu-icon tab-icon malibu-fill-gradient-purple" fill="#409EFF"/>
                                            <div class="service">Drycc Git</div>
                                            <small>Use Drycc CLI</small>
                                        </a>
                                    </li>
                                    <li class="deploy-tab tab-containers">
                                        <a @click="goToDryccImage" href="#" class="ember-view" :class="{'active': depolyType==='drycc-image'}">
                                            <icon-box size="2.5rem" class="icon malibu-icon tab-icon malibu-fill-gradient-purple" fill="#409EFF"/>
                                            <div class="service">Container</div>
                                            <small>Use Drycc CLI</small>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </li>

                    <deploy-drycc-git v-if="depolyType==='drycc-git'"/>
                    <deploy-drycc-image v-if="depolyType==='drycc-image'"/>
                </ul>
            </div>
        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AppDetailDeploy from "./AppDetailDeploy"
export default AppDetailDeploy
</script>

<style scoped>

</style>
