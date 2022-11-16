<template>
    <li class="list-group-item ember-view">
        <div class="panel-section ">
            <div class="section-description">
                <div class="section-title f3 purple" role="heading" aria-level="3">Config Vars</div>
                <div class="mt2 f5 lh-copy dark-gray">
                    Config vars change the way your app behaves. In addition to creating your own, some add-ons come with their own.
                </div>
            </div>

            <div class="panel-content" v-if="!showConfigVars">
                <div class="config-vars ember-view">
                    <button @click="showDetail" class="async-button default hk-button--secondary ember-view" type="submit">Reveal Config Vars</button>
                </div>
            </div>

            <div class="panel-content" v-if="showConfigVars">
                <div class="config-vars ember-view">
                    <button @click="closeDetail" class="fr async-button default hk-button--secondary ember-view" type="submit">Hide Config Vars</button>
                    <div class="config-vars-list ember-view">
                        <div class="group-header"><h5>Config Vars</h5></div>
                        <div class="mb5 hk-well ember-view" v-if="configVar">
                            <div class="f3 dark-gray lh-title mv1 ember-view">There are no config vars for this app yet</div>
                            <div class="f5 gray lh-copy ember-view">
                                <a href="https://www.drycc.cc/applications/managing-app-configuration/" class="hk-link" target="_blank">
                                    Learn about config vars
                                </a> in the Dev Center.
                            </div>
                        </div>
                        <form>
                            <table class="table editable-list purple-list config-vars-list-table">
                                <tbody>
                                <template v-for="(dealtConfig, index) in dealtConfigs">
                                <tr class="config-var-item ember-view">
                                    <td>
                                        <input readonly class="config-var-key monospace ember-text-field form-control ember-view" type="text" :value="dealtConfig.name">
                                    </td>
                                    <td>
                                        <textarea wrap="off" :id="index" rows="1" resize="false" v-bind:readonly="dealtConfig.isReadOnly" class="config-var-value monospace ember-text-area form-control ember-view">{{dealtConfig.value}}</textarea>
                                    </td>

                                    <td class="action-cell ember-view">
                                        <button @click="couldEdit(dealtConfig)" class="bg-transparent hk-focus-ring--blue:focus cursor-hand br1 ba0 b--none pa--1 pr3" title="Edit" type="button" >
                                            <span class="clip">Edit</span>
                                            <svg style="height: 20px; width: 20px;" class="icon malibu-icon malibu-fill-gradient-purple" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="16" height="16"><path d="M862.72 306.346667l60.16-60.16c20.053333-20.053333 20.053333-52.48 0-72.533334l-72.533333-72.533333c-20.053333-20.053333-52.48-20.053333-72.533334 0l-60.16 60.16 145.066667 145.066667zM669.44 209.493333L158.293333 720.64l-72.106666 217.173333 217.173333-72.106666L814.506667 354.56z" fill="#409EFF" ></path></svg>
                                        </button>
                                        <button @click="deleteConfig(index)" class="bg-transparent hk-focus-ring--blue:focus cursor-hand br1 ba0 b--none pa--1 mr2" title="Delete" type="button" >
                                            <span class="clip">Delete</span>
                                            <svg style="height: 16px; width: 16px;" class="icon malibu-icon fill-gray hover-fill-red" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="200" height="200"><path d="M574.55 522.35L904.4 192.5c16.65-16.65 16.65-44.1 0-60.75l-1.8-1.8c-16.65-16.65-44.1-16.65-60.75 0L512 460.25l-329.85-330.3c-16.65-16.65-44.1-16.65-60.75 0l-1.8 1.8c-17.1 16.65-17.1 44.1 0 60.75l329.85 329.85L119.6 852.2c-16.65 16.65-16.65 44.1 0 60.75l1.8 1.8c16.65 16.65 44.1 16.65 60.75 0L512 584.9l329.85 329.85c16.65 16.65 44.1 16.65 60.75 0l1.8-1.8c16.65-16.65 16.65-44.1 0-60.75L574.55 522.35z" ></path></svg>
                                        </button>
                                    </td>
                                </tr>
                                </template>

                                <tr class="config-var-new">
                                    <td>
                                        <div class="form-group ember-view">
                                            <input placeholder="KEY" v-model="newKey" class="form-control config-var-key monospace ember-text-field ember-view" type="text">
                                        </div>
                                    </td>

                                    <td>
                                        <div class="ember-view">
                                            <textarea placeholder="VALUE" v-model="newValue" wrap="off" rows="1" resize="false" class="config-var-value monospace form-control   ember-text-area ember-view">
                                            </textarea>
                                        </div>
                                    </td>

                                    <td class="config-var-add">
                                        <button @click="addConfig" :disabled="!newKey"
                                                :class="{'hk-button--disabled-primary': !newKey, 'hk-button--primary': newKey}"
                                                class="async-button default ember-view" type="button">    Add
                                        </button>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            <button :class="{'hk-button--disabled-primary':!isCommit}" :disabled="!isCommit"
                                    class="async-button default hk-button--success ember-view" type="button" @click="updateConfigs"> Save
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </li>
</template>

<script>
import SettingConfigVars from "./SettingConfigVars"
export default SettingConfigVars
</script>

<style scoped>

</style>
