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
                <main-nav :is-settings-active="true" :app-detail="appDetail"/>
                <ul class="list-group list-group-lg">
                    <setting-app-info :app-detail="appDetail"/>
                    <setting-config-vars />
    <!--                <setting-buildpacks />-->
                    <setting-domains />
                    <setting-transfer-ownership />
                    <setting-delete-app />
                </ul>
            </div>
        </div>
        <main-footer />
    </div>
</template>

<script>
import AppDetailSettings from  "./AppDetailSettings"
export default AppDetailSettings
</script>

<style scoped>

</style>
