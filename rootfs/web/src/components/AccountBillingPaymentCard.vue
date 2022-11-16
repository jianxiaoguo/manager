<template>
  <div id="hk-slide-panels">
    <div class="hk-slide-panel-overlay is-visible ember-view">
      <div
        class="hk-slide-panel-container shadow-outer-2 flex flex-column fixed bg-white overflow-y-hidden ma2 br2 from-right standard"
        data-test-target="slide-panel-container">
        <div
          class="hk-slide-panel-header relative flex justify-center tc items-center relative bb b--light-silver bg-white z-2 ember-view">
          <div class="ml4 flex-auto f3 dark-gray truncate lh-copy" data-test-target="slide-panel-header-title">
            Enter Your Payment Information
          </div>

          <button class="flex bg-transparent bn mr2 mt0 pa1 pointer" data-test-target="slide-panel-dismiss"
            aria-label="Dismiss slide panel" type="button" data-ember-action="" data-ember-action-149="149">
            <svg style="height: 16px; width: 16px;" class="icon malibu-icon fill-gray" data-test-icon-name="delete-16"
              aria-labelledby="malibu-icon-ember150" data-test-target="malibu-icon" aria-hidden="false" role="img">
              <title>Dismiss slide panel</title>
              <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#delete-16"></use>
            </svg>

          </button>
        </div>
        <div id="payment-form-panel"
          class="hk-slide-panel-content relative overflow-y-auto flex flex-column z-1 ember-view">
          <div class="flex flex-column h-100">
            <div class="slide-panel-shadow-cover-top z-5"></div>
            <div class="slide-panel-content flex-grow-1 flex-shrink-0 pa4">
              <div>
                <el-form class="flex justify-center w-100">
                  <div class="flex flex-column justify-between">
                    <div class="mb3 flex flex-column items-center justify-center">
                      <div class="w-100">
                        <div class="ember-view"> <label for="hosted-fields-number" class="hk-label ember-view">Card
                            number <span class="red tooltip-component ember-view"
                              data-original-title="Required">*</span>
                          </label>
                          <div class="hk-braintree-hosted-fields h3 ember-view" id="card-number"></div>
                        </div>
                      </div>
                    </div>
                    <div class="pb1 flex flex-column flex-row-ns items-center justify-center">
                      <div class="flex flex-1-ns w-100 flex-row-ns flex-column">
                        <div class="flex-1-ns w-100 mr2-ns mb0-ns pb2">
                          <div class="ember-view"> <label for="hosted-fields-expirationDate"
                              class="hk-label ember-view">Expiration <span title=""
                                class="red tooltip-component ember-view" data-original-title="Required">*</span>
                              <!---->
                            </label>
                            <div class="hk-braintree-hosted-fields h3 ember-view" id="card-expiry"></div>
                          </div>
                        </div>
                        <div class="flex-1-ns w-100 pb2">
                          <div class="ember-view"> <label for="hosted-fields-cvv"
                              class="hk-label ember-view">CVV <span
                                class="red tooltip-component ember-view" data-original-title="Required">*</span>
                              <!---->
                            </label>
                            <div class="hk-braintree-hosted-fields h3 ember-view" id="card-cvc"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="pb1 flex flex-column flex-row-ns items-center justify-center">
                      <div class="w-100 pb2">
                        <div class="ember-view"> <label for="fullname" class="db hk-label ember-view">Legal/Business
                            Name<span title="" class="red tooltip-component ember-view"
                              data-original-title="Required">*</span>
                            <!---->
                          </label>
                          <el-input v-model="billing_details.name" class="w-100 ember-view" autocomplete="billing family-name" />
                        </div>
                      </div>
                    </div>
                    <div class="pb1 flex flex-column items-center justify-center">
                      <div class="w-100 pb3">
                        <div class="ember-view"> <label for="billing-country" class="hk-label ember-view">Country <span
                              title="" class="red tooltip-component ember-view" data-original-title="Required">*</span>
                            <!---->
                          </label>
                          <el-select class="w-100 ember-view" v-model="billing_details.address.country" placeholder="Country">
                            <el-option class="x-option ember-view" v-for="item in countries" :key="item.code"
                              :label="item.name" :value="item.code" />
                          </el-select>
                        </div>
                      </div>
                      <div class="w-100 pb3">
                        <div class="ember-view"> <label for="billing-address" class="db hk-label ember-view">Billing
                            address line 1 <span title="" class="red tooltip-component ember-view"
                              data-original-title="Required">*</span>
                          </label>
                          <el-input v-model="billing_details.address.line1" class="w-100 ember-view" autocomplete="billing address-line1" />
                        </div>
                      </div>
                      <div class="w-100 pb2">
                        <div class="ember-view"> <label for="billing-address2" class="db hk-label ember-view">Billing
                            address line 2
                            <!---->
                          </label>
                          <el-input v-model="billing_details.address.line2" class="w-100 ember-view" autocomplete="billing address-line2" />
                        </div>
                      </div>
                    </div>
                    <div class="pb1 flex flex-column items-center justify-center">
                      <div class="w-100 pb3">
                        <div class="ember-view"> <label for="address-level2" class="db hk-label ember-view">City <span
                              title="" class="red tooltip-component ember-view" data-original-title="Required">*</span>
                            <!---->
                          </label>
                          <el-input v-model="billing_details.address.city" class="w-100 ember-view" autocomplete="billing address-level2" />
                        </div>
                      </div>
                      <div class="w-100 pb3">
                        <div class="ember-view"> <label for="address-level1"
                            class="db hk-label ember-view">State/Province <span title=""
                              class="red tooltip-component ember-view" data-original-title="Required">*</span>
                            <!---->
                          </label>
                          <el-input v-model="billing_details.address.state" class="w-100 ember-view" autocomplete="billing address-level1" />
                        </div>
                      </div>
                      <div class="flex-1-ns w-100 pb3">
                        <div class="ember-view"><label for="postal"
                            class="db hk-label ember-view"> Postal code
                            <span class="red tooltip-component ember-view"
                              data-original-title="Required">*</span>

                            <!---->
                          </label> 
                          <div class="hk-braintree-hosted-fields h3 ember-view" id="card-postcode"></div>
                        </div>
                      </div>
                      <!---->
                      <div class="w-100 pb3">
                        <div class="ember-view"> <label for="other" class="hk-label ember-view">Additional information
                            <!---->
                          </label>
                          <el-input class="w-100 ember-view" v-model="other" :rows="2" type="textarea"
                            autocomplete="billing address-level3" placeholder="(company name, tax ID, etc.)" />
                        </div>
                      </div>
                      <!---->
                    </div>
                  </div>
                </el-form>
              </div>

            </div>
            <div class="slide-panel-shadow-cover-bottom z-5"></div>
          </div>
        </div>
        <div class="hk-slide-panel-footer relative shadow-outer-1 flex justify-center items-center z-2 pa4 ember-view">
          <button @click="closePaymentCard" class="async-button w-50 mr2 default hk-button--secondary ember-view"
            type="button">
            Cancel
          </button>
          <button @click="savePaymentCard" form="payment-method-form"
            class="async-button w-50 default hk-button--primary ember-view" type="submit"> Save Details

          </button>
        </div>
      </div>

    </div>
  </div>
</template>
  <script>
import AccountBillingPaymentCard from "./AccountBillingPaymentCard"
export default AccountBillingPaymentCard
</script>

  <style scoped>
</style>
