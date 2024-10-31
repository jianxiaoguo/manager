<template>
    <div id="modal-overlays">
        <div class="ember-modal-overlay modal-overlay translucent ember-view">
            <div class="ember-modal-dialog ember-view">
                <div class="modal-box">
                    <div class="modal-header">
                        <h4 class="modal-title fw5">Rollback to {{currentActivity.v}}</h4>
                        <button class="bg-transparent hk-focus-ring--blue:focus cursor-hand br1 ba0 b--none pa--1 hk-button bg-transparent pa1 h-auto absolute right-1 top-1" title="Close modal">
                            <span class="clip">Close modal</span>
                            <svg style="height: 16px; width: 16px;"  class="icon malibu-icon fill-gray" data-test-icon-name="delete-16" data-test-target="malibu-icon" aria-hidden="true" role="img">
                                <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#delete-16"></use>
                            </svg>
                        </button>
                    </div>

                    <div class="modal-content">
                        <div class="modal-body ">
                            <div class="ember-view">
                                <div class="ph3">
                                    <div class="flex flex-column mb4 mt2 lh-copy">
                                        <div class="f4 dark-gray tc mb2">
                                            Confirm the result of rolling back to {{currentActivity.v}}
                                        </div>
                                        <div class="f5 dark-gray tc mb4">
                                            Rolling back to a previous release will
                                            <span class="b">restore the code from that release</span>
                                            as well as
                                            <span class="b">remove any config var changes</span>
                                            made since that release.
                                        </div>
                                        <div class="bg-lightest-orange inline-flex ba b--light-orange br1 pa2">
                                            <div class="f5 orange">
                                                Changes made to external resources will not be rolled back.
                                                Resources that set config vars may stop working if a release with
                                                a config var change is rolled back.
                                                <a href="https://www.drycc.cc/applications/managing-app-lifecycle/" target="_blank" class="hk-link orange">Learn more</a>.
                                            </div>
                                        </div>
                                    </div>

                                    <div class="f5 b dark-gray pl2 pb2">
                                        {{rollActivities.length}} release below will be rolled back
                                    </div>

                                    <div class="flex flex-column dark-gray lh-copy bt b--light-silver pa2" v-for="rollActivity in rollActivities">
                                        <div class="f5">
                                            <span class="b">{{rollActivity.v}}</span> ·
                                            <span :title="rollActivity.createdTime.format('yyyy.MM.dd hh:mm:ss')" class="timeago ember-view">{{rollActivity.createdTime.format("yyyy-MM-dd at hh:mm")}}</span>
                                        </div>
                                        <div class="f5">
                                            <span>{{rollActivity.username}}:</span>
                                            <span>{{rollActivity.content}}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="modal-footer flex justify-end">
                        <button class="btn btn-default" @click="closeRollBack">
                            Cancel
                        </button>

                        <button class="confirm-rollback btn btn-primary async-button default ember-view" @click="rollBack">
                            Rollback
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class=" modal-backdrop fixed absolute--fill pe-none"></div>
    </div>
</template>

<script>
import ActivityRollBack from "./ActivityRollBack"
export default ActivityRollBack
</script>

<style scoped>

</style>
