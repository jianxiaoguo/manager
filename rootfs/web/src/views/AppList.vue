<!--app列表页-->
<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box>
            <template v-slot:nav-cluster>
                <cluster-select />
            </template>
            <template v-slot:navbox-extension>
                <div>
                    <div class="btn-group ember-view">
                        <button @click="goToNewApp" class="drop-down__toggle hk-button--secondary pr1" style="color: #409EFF;">
                            Create New App
                        </button>
                    </div>
                </div>
            </template>
        </nav-box>
        <div class="main-content">
            <div class="mv3 limit-width">
                <div class="flex">
                    <icon-search class="icon malibu-icon fill-gray absolute z-2 ml2 mt1 nudge-down--3" />
                    <input 
                        placeholder="Press enter to filter apps" 
                        class="hk-search-input focus-z-1" 
                        autocapitalize="off" 
                        autocorrect="off" 
                        autocomplete="off" 
                        spellcheck="false" 
                        size="32"
                        v-model="name"
                        @keyup.enter="fetchAppList"
                    >
                </div>
            </div>
            <div class="app-list hk-hide-bb-last-row">
                <div :key="Math.random()" class="apps-list-item flex flex-column flex-auto b--light-silver bg-white pv2 ph4 bb hover-bg-near-white ember-view" v-for="item in apps">
                    <one-app :app="item"/>
                </div>
                <div class="limit-width bg-white mt4 pager">
                    <el-pagination
                    layout="prev, pager, next"
                    :page-size="pageSize"
                    :current-page="page"
                    :hide-on-single-page="true"
                    @current-change="pageCurrentChange"
                    :total="count">
                    </el-pagination>
                </div>
                <div class="bg-white pv3 bt justify-center flex ember-view"></div>
            </div>
        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AppList from  "./AppList"
export default AppList
</script>

<style scoped>
    .pr1 {
        padding-right: 15px;
    }
</style>
