<!--集群选择器-->
<template>
<div id="'vue-content'+Math.random()" class="crumb-trail flex items-center flex-auto f3 lh-copy dark-gray nudge-left--5 pv--3 ember-view">
    <cluster-select class="ml1"/>
    <span class="flex items-center mb1">
        <span class="inline-flex pv--2 mr--2">
            <div class="relative ember-view mt1">
                <icon-application-one class="icon malibu-icon v-mid" fill="#409EFF" />
            </div>
        </span>
        <span>
            {{ appDetail.name }}
        </span>
    </span>
</div>
</template>

<script>
import ClusterSelectAppDetail from "./ClusterSelectAppDetail"
export default ClusterSelectAppDetail
</script>

<style scoped>
    .context-switcher__list {
        width: 160px;
    }
    .bg-lightest-purple {
        background: #ffffff;
    }
</style>
