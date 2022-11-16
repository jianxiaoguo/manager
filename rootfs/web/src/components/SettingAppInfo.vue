<template>
    <li class="list-group-item ember-view">
        <div class="panel-section ">
            <div class="section-description">
                <div class="section-title f3 purple" role="heading" aria-level="3">
                    App Information
                </div>
            </div>

            <div class="panel-content">
                <div>
                    <div class="ember-view">
                        <div class="w-100 flex mb2 items-center">
                            <div class="w-20 hk-label mv1">Name</div>
                            <div class="w-80 flex items-center">
                                {{ appDetail.name }}
                            </div>
                        </div>


                        <div class="w-100 flex mb2 items-center">
                            <div class="w-20 hk-label mv1">Owner</div>
                            <div class="w-80 flex items-center">
                                {{ appDetail.owner }}
                            </div>
                        </div>

                        <div class="w-100 flex mb2 items-center">
                            <div class="w-20 hk-label mv1">Created</div>
                           <div class="w-80 flex items-center">
                               {{ appDetail.created }}
                           </div>
                        </div>
                        <div class="w-100 flex mb2 items-center">
                            <div class="w-20 hk-label mv1">Updated</div>
                            <div>
                                <span class="gray">{{ appDetail.updated }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </li>
</template>

<script>
import SettingAppInfo from "./SettingAppInfo"
export default SettingAppInfo
</script>

<style scoped>

</style>
