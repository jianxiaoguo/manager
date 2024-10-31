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
            <main-nav :is-resources-active="true" :app-detail="appDetail"/>
            <resources-dyno :app-detail="appDetail"/>
            <resources-volume :app-detail="appDetail"/>
            <resources-addons :app-detail="appDetail"/>
<!--            <div class="app-resource-total-line-item limit-width">-->
<!--                <small class="line-item-label"> Estimated Monthly Cost </small>-->
<!--                <div class="line-item-values"><span class="line-item-original-value ">￥0.00</span></div>-->
<!--            </div>-->
        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AppDetailResources from  "./AppDetailResources"
export default AppDetailResources
</script>

<style scoped>

</style>
