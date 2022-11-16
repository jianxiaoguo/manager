<template>
    <li class="list-group-item ember-view"><div class="panel-section danger app-deletion">
        <div class="section-description">
            <div class="section-title f3 purple" role="heading" aria-level="3">
                Delete App
                <!---->    </div>

            <div class="mt2 f5 lh-copy dark-gray">
                Deleting your app and its add-ons is irreversible.
            </div>

            <!---->  </div>

        <div class="panel-content">
            <p>
<span class="confirmable-action ember-view">  <button @click="deleteAppBTN" class="hk-button--danger delete-app" data-ember-action="" data-ember-action-124="124">
    Delete app...
  </button>

    <!----></span>    </p>

        </div>
    </div>
    </li>
</template>

<script>
import SettingDeleteApp from "./SettingDeleteApp"
export default SettingDeleteApp
</script>

<style scoped>

</style>
