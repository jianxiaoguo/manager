<template>
    <ul class="list-group list-group-lg">
        <li class="list-group-item ember-view">
            <div class="panel-section">
                <div class="section-description">
                    <div class="section-title f3 bule">Profile</div>
                    <div class="mt2 f5 lh-copy dark-gray">
                        Your email address is your identity on Drycc and is used to log in.
                    </div>
                </div>

                <div class="panel-content">
                    <div class="profile edit-first">
                        <div class="ember-view">
                            <div class="ember-view">
                                <label class="hk-label db mb2">Username (Optional)</label>
                                <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                    <input class="mr2 mb2 w-100 mw6 ember-text-field hk-input--read-only ember-view"
                                        type="text" disabled="disabled" :value="user.username">
                                </div>
                            </div>
                        </div>
                        <div class="ember-view">
                            <div class="ember-view">
                                <label class="hk-label db mb2">Email Address</label>
                                <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                    <input class="mr2 mb2 w-100 mw6 ember-text-field hk-input--read-only ember-view"
                                        type="text" disabled="disabled" :value="user.email">
                                </div>
                            </div>
                            <span class="confirmable-action ember-view"></span>
                        </div>
                        <div class="ember-view">
                            <div class="ember-view">
                                <label class="hk-label db mb2">First Name</label>
                                <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                    <input class="mr2 mb2 w-100 mw6 ember-text-field hk-input--read-only ember-view"
                                        type="text" disabled="disabled" :value="user.first_name">
                                </div>
                            </div>
                            <span class="confirmable-action ember-view"></span>
                        </div>
                        <div class="ember-view">
                            <div class="ember-view">
                                <label class="hk-label db mb2">Last Name</label>
                                <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                    <input class="mr2 mb2 w-100 mw6 ember-text-field hk-input--read-only ember-view"
                                        type="text" disabled="disabled" :value="user.last_name">
                                </div>
                            </div>
                            <span class="confirmable-action ember-view"></span>
                        </div>
                        <p class="f5 dark-gray">Manage your avatar using <a href="https://gravatar.com" target="_blank"
                                class="hk-link">Gravatar</a>.</p>
                    </div>
                </div>
            </div>
        </li>
        <li class="list-group-item ember-view">
            <div class="panel-section">
                <div class="section-description">
                    <div class="section-title f3 bule">Platform Credits</div>
                    <div class="mt2 f5 lh-copy dark-gray">
                        Platform Credits will be applied only to offset eligible fees.
                    </div>
                </div>

                <div class="panel-content">
                    <div class="profile edit-first">
                        <div class="ember-view">
                            <label class="hk-label db mb2">Credits</label>
                            <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                <input class="mr2 mb2 w-100 mw6 ember-text-field hk-input--read-only ember-view"
                                    type="text" disabled="disabled" :value="this.$toPrice(balance.amount)">
                            </div>
                        </div>
                        <div class="ember-view">
                            <div class="ember-view">
                                <label class="hk-label db mb2">Status</label>
                                <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                    <input class="mr2 mb2 w-100 mw6 ember-text-field hk-input--read-only ember-view"
                                        type="text" disabled="disabled"
                                        :value="balance.status == 1 ? 'normal' : 'frozen'">
                                </div>
                            </div>
                            <span class="confirmable-action ember-view"></span>
                        </div>
                        <div class="ember-view">
                            <div class="ember-view">
                                <label class="hk-label db mb2">Created Time</label>
                                <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                    <input class="mr2 mb2 w-100 mw6 ember-text-field hk-input--read-only ember-view"
                                        type="text" disabled="disabled" :value="balance.created">
                                </div>
                            </div>
                            <span class="confirmable-action ember-view"></span>
                        </div>
                        <div class="ember-view">
                            <div class="ember-view">
                                <label class="hk-label db mb2">Updated Time</label>
                                <div class="flex flex-column flex-row-ns items-center-ns w-100">
                                    <input class="mr2 mb2 w-100 mw6 ember-text-field hk-input--read-only ember-view"
                                        type="text" disabled="disabled" :value="balance.updated">
                                </div>
                            </div>
                            <span class="confirmable-action ember-view"></span>
                        </div>
                    </div>
                </div>
            </div>
        </li>
    </ul>

</template>

<script>
import AccountSettingProfile from "./AccountSettingProfile"
export default AccountSettingProfile
</script>

<style scoped>
</style>
