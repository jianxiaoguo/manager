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
            <main-nav :is-overview-active="true" :app-detail="appDetail"/>
            <div id="overview-page">
                <div class="overview-content">
                    <div class="limit-width">
<!--                        <overview-metrics :app-detail="appDetail"/>-->
                        <overview-appinfo :app-detail="appDetail"/>
                        <overview-volume :app-detail="appDetail"/>
                        <overview-addons :app-detail="appDetail"/>
                        <overview-formation :app-detail="appDetail"/>
                        <overview-collaborator-activity :app-detail="appDetail" />
                    </div>
                </div>
                <div class="overview-activity">
                    <div class="app-overview-stream">
                        <overview-latest-activity :app-detail="appDetail" />
                    </div>
                </div>
            </div>
        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AppDetailOverview from  "./AppDetailOverview"
export default AppDetailOverview
</script>

<style scoped>

</style>
