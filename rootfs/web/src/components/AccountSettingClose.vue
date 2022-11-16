<template>
    <div class="panel-section danger">
        <div class="section-description">
            <div class="section-title f3 purple">Close Account</div>
            <div class="mt2 f5 lh-copy dark-gray">
                You must delete all apps on this account first. <br><strong>Warning:</strong> Closing your account is irreversible.
            </div>
        </div>

        <div class="panel-content">
            <div class="ember-view">
                <span class="confirmable-action ember-view">
                    <button class="hk-button--danger" >
                        Close this account...
                    </button>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
import AccountSettingClose from "./AccountSettingClose"
export default AccountSettingClose
</script>

<style scoped>

</style>
