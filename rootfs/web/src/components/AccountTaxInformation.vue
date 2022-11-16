<template>
  <div class="panel-section">
    <div class="section-description">
      <div class="section-title f3 purple" role="heading" aria-level="3">
        Tax Information
        <!---->
      </div>

      <div class="mt2 f5 lh-copy dark-gray">
        We need to collect this information to submit accurate tax reports.
      </div>
    </div>
    <div class="panel-content" v-if="paymentCard == ''">
      <div class="hk-well ember-view">
        <div class="f3 dark-gray lh-title mv1 ember-view">
          Tax information management is not available
        </div>
        <div class="f5 gray lh-copy ember-view"> You may set an tax information once you have added a credit card to
          your account
        </div>
      </div>
    </div>
    <div class="panel-content" v-else>
      <div class="ember-view">
        <div class="measure-wide">
          <input placeholder="Tax no." class="hk-input mb2 w-100 ember-text-field ember-view" type="text"
            v-model="consumerTaxInfo.no" :disabled="consumerTaxInfo.status==1" @focus="editEditConsumerTaxInfo">

          <el-select class="mb2 w-100 ember-text-field ember-view" v-model="consumerTaxInfo.type" placeholder="Type"
            :disabled="consumerTaxInfo.status==1" @focus="editEditConsumerTaxInfo">
            <el-option v-for="item in consumerTaxInfoTypes" :key="item[0]"
              :label="item[1]" :value="item[0]" />
          </el-select>

          <el-select class="mb2 w-100 ember-text-field ember-view" v-model="consumerTaxInfo.country" placeholder="Country"
          :disabled="consumerTaxInfo.status==1" @focus="editEditConsumerTaxInfo">
            <el-option v-for="item in countries" :key="item.code"
              :label="item.name" :value="item.code" />
          </el-select>

          <div class="flex-ns flex-row items-center mb0 mb2-ns">
            <input placeholder="City" class="hk-input mb2 mb0-ns flex-auto w-100 w-50-ns ember-text-field ember-view"
              type="text" v-model="consumerTaxInfo.city" :disabled="consumerTaxInfo.status==1" @focus="editEditConsumerTaxInfo">

            <div class="w0 w1-ns"></div>

            <input placeholder="State/Province" class="hk-input mb2 mb0-ns w-100 w-50-ns ember-text-field ember-view"
              type="text" v-model="consumerTaxInfo.state" :disabled="consumerTaxInfo.status==1" @focus="editEditConsumerTaxInfo">
          </div>
          <p class="f5 dark-gray" v-if="consumerTaxInfo.status==1">If you need to modify tax information, please <a href="https://tawk.to/chat/6234b5491ffac05b1d7f4669/1fueu8a9t" target="_blank" class="hk-link">contact us</a>.</p>
        </div>

        <div class="measure-wide flex items-center" v-if="editEnabled">
          <button class="async-button default hk-button-sm--primary ember-view" @click="saveConsumerTaxInfo"> Save
          </button>
          <button class="async-button default hk-button-sm--tertiary ember-view" @click="canelEditConsumerTaxInfo">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AccountTaxInformation from "./AccountTaxInformation";
export default AccountTaxInformation;
</script>

<style scoped>
</style>
