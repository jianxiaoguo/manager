<!--集群选择器-->
<template>
<div id="'vue-content'+Math.random()" class="crumb-trail flex items-center flex-auto f3 lh-copy dark-gray nudge-left--5 pv--3 ember-view">
    <div class="flex items-center">
        <el-breadcrumb class="ml2 mt2">
            <div class="dib pv--1 pull-left">
                <icon-server class="icon malibu-icon" fill="#409EFF"/>
            </div>
            <el-breadcrumb-item class="f3 ml2 mr1 mb1" :to="{ path: '/' }">{{currentCluster.name}}</el-breadcrumb-item>
            <el-breadcrumb-item class="f3">{{ appDetail.name }}</el-breadcrumb-item>
        </el-breadcrumb>
    </div>
</div>
</template>

<script>
import ClusterAppDetail from "./ClusterAppDetail"
export default ClusterAppDetail
</script>

<style scoped>
    .context-switcher__list {
        width: 160px;
    }
    .bg-lightest-purple {
        background: #ffffff;
    }
</style>
