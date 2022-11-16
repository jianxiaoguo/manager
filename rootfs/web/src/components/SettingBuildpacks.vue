<template>
    <li class="list-group-item ember-view"><div class="panel-section ">
        <div class="section-description">
            <div class="section-title f3 purple" role="heading" aria-level="3">
                Buildpacks
                <!---->    </div>

            <div class="mt2 f5 lh-copy dark-gray">
                Buildpacks are scripts that are run when your app is deployed. They are used to install dependencies for your app and configure your environment. <a href="https://www.drycc.cc/applications/using-buildpacks/" class="hk-link">Find new buildpacks on Heroku Elements</a>
            </div>

            <!---->  </div>

        <div class="panel-content">
            <div class="buildpack-installations-list ember-view"><!---->
                <!---->
                <div class="flex bg-lightest-silver pa2 br--top br1 bb b--silver mb2">
                    <div class="flex-auto"></div>
                    <button class="async-button default hk-button--primary ember-view" type="submit">    Add buildpack
                    </button>
                </div>

                <div class="hk-well ember-view"><div class="f3 dark-gray lh-title mv1 ember-view">      Buildpacks will appear here

                </div><div class="f5 gray lh-copy ember-view">      Buildpacks are used to install dependencies for your app and configure your environment.

                </div></div>

                <!---->
                <!----></div>

        </div>
    </div>
    </li>
</template>

<script>
import SettingBuildpacks from "./SettingBuildpacks"
export default SettingBuildpacks
</script>

<style scoped>

</style>
