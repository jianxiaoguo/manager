<!--集群选择器-->
<template>
    <div class="flex items-center">
        <el-dropdown trigger="click" class="ml1 mt1">
            <span class="el-dropdown-link">
                <span class="dib pv--1">
                    <icon-server class="icon malibu-icon" fill="#409EFF"/>
                </span>
                <span class="f3 ml2 mr1 mb1 bule">{{currentCluster.name}}</span>
                <icon-down class="icon malibu-icon mr2" fill="#409EFF"/>
            </span>
            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item v-for="cluster in clusters">
                        <router-link :to="{path:'/apps'}" @click="changeCluster(cluster)">
                            <icon-server class="icon malibu-icon mr2" fill="#409EFF"/>
                            <span class="mb1">{{cluster.name}}</span>
                        </router-link>
                    </el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
    </div>
</template>

<script>
import ClusterSelect from "./ClusterSelect"
export default ClusterSelect
</script>

<style scoped>
    .el-dropdown-link span {
        font-weight: 700;
    }
    .context-switcher__list {
        width: 160px;
    }
    .bg-lightest-bule {
        background: #ffffff;
    }
</style>
