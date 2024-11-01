<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <setting-domain-add v-if="isShowEdit"
                              :editAccess="editAccess"
                              :domainDetail="domains"
                              @closeEdit="closeEdit"
    />
    <setting-domain-delete ref="settingDomainDelete" v-if="isShowDelete"
                        :editAccess="editAccess"
                        :domain="domain"
                        @closeDelete="closeDelete"
    />
    <li class="list-group-item ember-view"><div class="panel-section ">
        <div class="section-description">
            <div class="section-title f3 bule" role="heading" aria-level="3">
                Domains
            </div>

            <div class="mt2 f5 lh-copy dark-gray">
                You can add custom domains to any Drycc app.
            </div>
        </div>

        <div class="panel-content">
            <div class="domains-list ember-view">
                <div class="flex items-center pv2 br--top br1 bb b--silver mb1">
                    <div class="flex-auto gray">
                        Your app can be found at
                      <span v-if="domains.length>0">
                        <a :href="'http://' + domains[0].domain" target="_blank" class="hk-link">{{ domains[0].domain }}/</a>
                      </span>
                    </div>
                    <button class="async-button nowrap default async-button default hk-button--primary ember-view" type="submit" @click="showEdit()">    Add domain
                    </button>
                </div>
                <div class="hk-well ember-view" v-if="domains.length<0">
                    <div class="f3 dark-gray lh-title mv1 ember-view">
                      Custom domains will appear here
                    </div>
                    <div class="f5 gray lh-copy ember-view">
                      Custom domains allow you to access your app via one or more non-Drycc domain names (for example, <code>www.yourcustomdomain.com</code>)
                    </div>
                </div>

                <div class="flex justify-between pv2 mb2" v-if="domains.length>0">
<!--                  <div class="w-30 relative">-->
<!--                    <svg style="height: 16px; width: 16px;"  class="icon malibu-icon fill-gray absolute z-2 ml2 mt1 nudge-down&#45;&#45;3" data-test-icon-name="search-16" data-test-target="malibu-icon" aria-hidden="true" role="img">-->
<!--                      &lt;!&ndash;&ndash;&gt;  <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#search-16"></use>-->
<!--                    </svg>-->

<!--                    <input id="domains-list-filter" placeholder="Filter domains" aria-label="Filter domains" class="hk-search-input focus-z-1 w-100" autocapitalize="off" autocorrect="off" autocomplete="off" spellcheck="false" required="false">-->
<!--                  </div>-->
                  <div class="flex-auto"></div>
                  <div></div>
                </div>

                <form v-if="domains.length>0">
                  <table class="table editable-list table-auto bule-list domains-list-table">
                    <thead>
                    <tr>
                      <th class="pa0">Domain Name</th>
                      <th></th>
                    </tr>
                    </thead>
                    <tbody>
                      <template v-for="(domain, index) in domains">
                        <tr class="domain-item ember-view">
                          <td title="drycc-chart.uucin.com">
                            <div class="pl2">
                              <input readonly="" class="w-100 ember-text-field form-control ember-view" type="text" :value="domain.domain">
                            </div>
                          </td>
                          <td class="w2 action-cell ember-view">
                            <button @click="showDelete(index)" class="bg-transparent hk-focus-ring--blue:focus cursor-hand br1 ba0 b--none pa--1 mr2" title="Delete" type="button" >
<!--                              <span class="clip">Delete</span>-->
                              <svg style="height: 16px; width: 16px;" class="icon malibu-icon fill-gray hover-fill-red" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="200" height="200"><path d="M574.55 522.35L904.4 192.5c16.65-16.65 16.65-44.1 0-60.75l-1.8-1.8c-16.65-16.65-44.1-16.65-60.75 0L512 460.25l-329.85-330.3c-16.65-16.65-44.1-16.65-60.75 0l-1.8 1.8c-17.1 16.65-17.1 44.1 0 60.75l329.85 329.85L119.6 852.2c-16.65 16.65-16.65 44.1 0 60.75l1.8 1.8c16.65 16.65 44.1 16.65 60.75 0L512 584.9l329.85 329.85c16.65 16.65 44.1 16.65 60.75 0l1.8-1.8c16.65-16.65 16.65-44.1 0-60.75L574.55 522.35z" ></path></svg>
                            </button>
                          </td>
                        </tr>
                      </template>
                    </tbody>
                  </table>
                </form>

                <div class="bg-white pv3 justify-center flex flex ember-view">
                </div>
            </div>
        </div>
    </div>
    </li>
</div>
</template>

<script>
import SettingDomains from "./SettingDomains"
export default SettingDomains
</script>

<style scoped>

</style>
