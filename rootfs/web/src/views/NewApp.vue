<!--app列表页-->
<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box >
            <template v-slot:nav-cluster>
                <span class="link dark-gray center">
                    Create New App
                </span>
            </template>
            <template v-slot:navbox-extension>
                <div></div>
            </template>
        </nav-box>
        <div class="main-content">
            <form class="new-app-view relative flex justify-center pv6">
                <div class="w-100 mw7">
                    <div class="f5 b dark-gray mb2">App name</div>
                    <div class="new-app-name mb3 ember-view">
                        <div class="flex w-100">
                            <input v-model="appName" autocomplete="off" placeholder="app-name" maxlength="30" class="ember-text-field ember-view hk-input w-100" type="text">
                        </div>
                    </div>

                    <div class="runtime-selection ember-view">
                        <div class="f5 b dark-gray mb2">Choose a cluster</div>
                        <div class="relative region-selection">
                            <icon-server class="icon malibu-icon fill-gray absolute z-2 ml2 mt1 nudge-down--3" />
                            <select tabindex="0" v-model="selectedClusterId" class="hk-select pl6 w-100 x-select ember-view">

                                <option class="x-option ember-view" v-for="item in clusters" :value='item.uuid'>{{item.name}}</option>

                            </select>
                        </div>
                    </div>

                    <div class="mv4 bb b--light-silver"></div>

                    <button class="async-button default hk-button--primary create-app-button ember-view" @click="createNewApp" type="button">    Create app
                    </button>

                </div>
            </form>
        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import NewApp from "./NewApp"
export default NewApp
</script>

<style scoped>
    p.center{
        text-align: center;
    }
</style>
