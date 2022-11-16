<template>
    <li class="list-group-item ember-view"><div class="panel-section ">
        <div class="section-description">
            <div class="section-title f3 purple" role="heading" aria-level="3">
                Transfer Ownership
                <!---->    </div>

            <div class="mt2 f5 lh-copy dark-gray">
                Transfer this app to your personal account or a team you are a member of. <a href="https://www.drycc.cc/users/cli/" class="hk-link" target="blank">Learn more</a>
            </div>

            <!---->  </div>

      <div class="panel-content">
        <div class="ember-view">
          <div class="w-100 w-60-ns">
            <div class="f5 b mb2 dark-gray">Choose app owner</div>
            <div class="flex mb3">
              <icon-user class="icon malibu-icon fill-gray absolute z-2 ml2 mt1"/>
              <input placeholder="username" class="hk-input flex-auto pl6 ember-text-field ember-view" required
                     type="text" v-model="username">
              <div id="ember-basic-dropdown-content-ember111" class="ember-basic-dropdown-content-placeholder"
                   style="display: none;"></div>


            </div>
            <!--                <button class="async-button default hk-button&#45;&#45;disabled-primary ember-view" type="button" @click="transferOwnership">    Transfer app...</button>-->
            <button :class="{'hk-button--disabled-primary':!username}" :disabled="!username"
                    class="async-button default hk-button--success ember-view" type="submit " @click="transferOwnership"> Transfer app...
            </button>
          </div>

                <!----></div>

        </div>
    </div>
    </li>
</template>

<script>
import SettingTransferOwnership from "./SettingTransferOwnership"
export default SettingTransferOwnership
</script>

<style scoped>
button[disabled]{
  cursor: not-allowed;
}
</style>
