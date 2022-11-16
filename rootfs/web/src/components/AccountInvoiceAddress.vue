<template>
  <div class="panel-section">
    <div class="section-description">
      <div class="section-title f3 purple" role="heading" aria-level="3">
        Invoice Address
        <!---->
      </div>

      <div class="mt2 f5 lh-copy dark-gray">
        We'll print this address on your invoices. If blank, we'll use your billing address instead.
      </div>
    </div>

    <div class="panel-content" v-if="paymentCard == ''">
      <div class="hk-well ember-view">
        <div class="f3 dark-gray lh-title mv1 ember-view"> Invoice Address management is not available

        </div>
        <div class="f5 gray lh-copy ember-view"> You may set an invoice address once you have added a credit card to
          your account
        </div>
      </div>
    </div>
    <div class="panel-content" v-else-if="editEnabled">
      <div class="ember-view">
        <div class="measure-wide">
          <input placeholder="Address Line 1" class="hk-input mb2 w-100 ember-text-field ember-view" type="text"
            v-model="invoiceAddress.address1">

          <input placeholder="Address Line 2" class="hk-input mb2 w-100 ember-text-field ember-view" type="text"
            v-model="invoiceAddress.address2">

          <el-select class="mb2 w-100 ember-text-field ember-view" v-model="invoiceAddress.country" placeholder="Country">
            <el-option v-for="item in countries" :key="item.code"
              :label="item.name" :value="item.code" />
          </el-select>

          <div class="flex-ns flex-row items-center mb0 mb2-ns">
            <input placeholder="City" class="hk-input mb2 mb0-ns flex-auto w-100 w-50-ns ember-text-field ember-view"
              type="text" v-model="invoiceAddress.city">

            <div class="w0 w1-ns"></div>

            <input placeholder="State/Province" class="hk-input mb2 mb0-ns w-100 w-50-ns ember-text-field ember-view"
              type="text" v-model="invoiceAddress.state">

            <div class="w0 w1-ns"></div>

            <input placeholder="Postal Code" class="hk-input mb2 mb0-ns w-100 w5-ns ember-text-field ember-view"
              type="text" v-model="invoiceAddress.postcode">
          </div>


          <textarea placeholder="(company name, tax ID, etc.)" class="hk-input w-100 mb2 ember-text-area ember-view"
            v-model="invoiceAddress.other"></textarea>

        </div>

        <div class="measure-wide flex items-center">
          <button class="async-button default hk-button-sm--primary ember-view" @click="saveInvoiceAddress"> Save
          </button>
          <button class="async-button default hk-button-sm--tertiary ember-view" @click="canelEditInvoiceAddress">
            Cancel
          </button>
          <div class="flex-auto"></div>
          <button class="async-button default hk-button-sm--danger ember-view" @click="removeInvoiceAddress"> Remove
            invoice address
          </button>
        </div>
      </div>
    </div>
    <div class="panel-content" v-else-if="!nullAddress">
      <div class="ember-view">
        <div class="mb3">
          <div class="">{{ invoiceAddress.address1 }}</div>
          <div class="">{{ invoiceAddress.address2 }}</div>
          <div class="">{{ invoiceAddress.city }}, {{ invoiceAddress.state }} {{ invoiceAddress.postcode }}</div>
          <div class="">{{ invoiceAddress.country }}</div>
          <div class="">{{ invoiceAddress.other }}</div>
        </div>
        <button class="async-button default hk-button-sm--primary ember-view" @click="editInvoiceAddress">
          Edit
        </button>
      </div>
    </div>
    <div class="panel-content" v-else>
      <div class="ember-view">
        <button class="async-button default hk-button--secondary ember-view" @click="editInvoiceAddress">
          Add invoice address
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import AccountInvoiceAddress from "./AccountInvoiceAddress";
export default AccountInvoiceAddress;
</script>

<style scoped>
</style>
