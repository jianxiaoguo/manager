<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box>
            <template v-slot:nav-cluster>
                <a href="/account" class="link dark-gray active ember-view">Manage Account</a>
            </template>
            <template v-slot:navbox-extension>

            </template>
        </nav-box>
        <div class="main-content">
            <nav class="account-nav nav nav-tabs sub-nav ember-view">
                <div class="limit-width">
                    <div class="sub-nav-item ember-view">
                        <a href="#" @click="goToAccountSetting" class="active ember-view">
                            <span class="sub-nav-item-name gray">Account</span>
                        </a>
                    </div>
                    <div class="account-application-nav sub-nav-item ember-view">
                        <a href="#" @click="goToAccountFunding" class="ember-view">
                            <span class="sub-nav-item-name gray">Funding</span>
                        </a>
                    </div>
                    <div class="account-application-nav sub-nav-item ember-view">
                        <a href="#" @click="goToAccountBilling" class="ember-view">
                            <span class="sub-nav-item-name gray">Billing</span>
                        </a>
                    </div>
                </div>
            </nav>
            <account-setting-profile />
        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AccountSetting from "./AccountSetting"
export default AccountSetting
</script>

<style scoped>

</style>
