<template>
    <div class="ember-view">
        <div class="dib w-100 flex-ns items-center pv2">
            <div class="flex dark-gray mr2">
                <div class="mr1">App Info</div>
            </div>
            <div class="flex-auto"></div>
        </div>
        <div class="bule-box">
            <div class="ph3 pv1">
                <div class="formation-tier">
                  <b>Application</b>
                </div>
                <div class="collaborator f5 ember-view">
                  <div class="bule-box">
                    <template v-for="(value, name, index) in appDetail">
                      <div class="display-formation-list hk-hide-bb-last-row ember-view">
                        <div class="flex pa3 items-center bb b--light-silver">
                          <div class="mr3 flex-auto">
                            <div class="flex flex-row">
                              <div class="mr2 w-60 hk-label mv1">{{name}}</div>
                              <div class="mid-gray f5 code truncate w-40 flex items-center" :title="value">{{value}}</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </template>
                  </div>
                </div>
            </div>

            <div class="ph3 pv1">
              <div class="formation-tier">
                <b>Domains</b>
              </div>
              <div class="collaborator f5 ember-view">
                <div class="bule-box">
                  <template v-for="domain in domains">
                    <div class="display-formation-list hk-hide-bb-last-row ember-view" >
                      <div class="flex pa3 items-center bb b--light-silver">
                        <div class="mr3 flex-auto">
                          <div class="flex flex-row w-90">
                            <div class="mr2">{{domain.domain}}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>
                </div>
              </div>
            </div>

            <div style="display:none" class="ph3 pv1">
              <div class="formation-tier">
                <b>Processes</b>
              </div>
              <div class="collaborator f5 ember-view">
                <div class="bule-box">
                  <template v-for="p in ps">
                    <div class="display-formation-list hk-hide-bb-last-row ember-view" >
                      <div class="flex pa3 items-center bb b--light-silver">
                        <div class="mr3 flex-auto">
                          <div class="flex flex-row w-90">
                            <div class="mr2">p.type p.status (p.replicas) </div>
                            <div v-for="p in p.podsList">
                              <div class="mid-gray f5 code truncate">{{"%s %s (%s)", pod.name, pod.state, pod.release}}</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>
                </div>
              </div>
            </div>

        </div>
    </div>
</template>

<script>
import OverviewAppInfo from "./OverviewAppInfo"
export default OverviewAppInfo
</script>

<style scoped>
    a:hover {
        cursor: pointer;
    }
</style>
