<template>
    <div class="ember-view">
        <div class="flex-ns items-center pv2">
            <div class="flex dark-gray mr2">
                <div class="mr1">Dyno formation</div>
            </div>
            <div class="flex-auto"></div>

            <a @click="goToResources" class="flex items-center hk-link no-underline f6 mv1 mv0-ns ember-view">
                <span class="underline">Details Ptypes</span>
                 <icon-arrow-circle-right class="ml--3 nudge-down--1" size="1.2rem"/>
            </a>
        </div>

        <div class="purple-box" v-if="processes.length > 0">
            <div class="formation-tier">
                <p>This app is using {{processes.length}} ptypes</p>
            </div>
            <template v-for="process in processes">
            <div class="display-formation-list hk-hide-bb-last-row ember-view">
                <div class="flex pa3 items-center bb b--light-silver">
                    <div class="mr3 flex-auto">
                        <div class="flex flex-row w-90">
                            <div class="mr2">{{process.name}}</div>
                            <div class="mid-gray f5 code truncate">{{process.cmd}}</div>
                        </div>
                    </div>
                    <span class="text-uppercase b f5">
                        <span class="light-green" v-if="process.status === 1">On</span>
                        <span class="light-red" v-if="process.status === 0">Off</span>
                    </span>
                </div>
            </div>
            </template>
        </div>

        <div class="mb5 ember-view" v-if="processes.length === 0">
            <div class="hk-well ember-view">
                <div class="f3 dark-gray lh-title mv1 ember-view">
                    This app has no process types yet
                </div>
                <div class="f5 gray lh-copy ember-view">
                    Add a Procfile to your app in order to define its process types
                    <a href="https://www.drycc.cc/applications/managing-app-processes" class="hk-link" target="_blank">Learn more</a>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import OverviewFormation from "./OverviewFormation"
export default OverviewFormation
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
</style>
