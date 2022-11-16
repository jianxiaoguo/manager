<template>
  <div class="panel-section">
    <account-bill-payment-card :publicKey="publicKey" v-if="editPaymentCard" @closePaymentCardAction="closePaymentCardAction" />
    <div class="section-description">
      <div class="section-title f3 purple">Billing Information</div>
    </div>

    <div class="panel-content">
      <template  v-if="publicKey != null && publicKey !== ''">
      <div id="update-credit-card" v-if="paymentCard === ''">
        <div class="ember-view">
          <!---->
          <div
            class="
              flex
              items-center
              flex-wrap
              bg-white
              br2
              shadow-outer-1
              ph3
              pv2
            "
          >
            <div class="flex items-center flex-auto dark-gray lh-copy">
              <span class="f4">This account does not have a credit card.</span>
            </div>
            <div class="pv1">
              <button
                @click="editPaymentCardAction"
                class="async-button default hk-button--primary ember-view"
                type="submit"
              >
                Add credit card
              </button>
            </div>
          </div>
          <!---->
        </div>
      </div>
      <div id="update-credit-card" v-else>
        <div class="ember-view">
          <!---->
          <div
            class="
              flex
              items-center
              flex-wrap
              bg-white
              br2
              shadow-outer-1
              ph3
              pv2
            "
          >
            <div class="flex items-center flex-auto">
              <div class="inline-flex mr3 ember-view">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="40"
                  height="26"
                  viewBox="0 0 40 26"
                >
                  <defs>
                    <linearGradient
                      id="dLvChIa"
                      x1="50%"
                      x2="50%"
                      y1="0%"
                      y2="100%"
                    >
                      <stop offset="0%" stop-color="#FFF"></stop>
                      <stop offset="100%" stop-color="#FFF7EB"></stop>
                    </linearGradient>
                  </defs>
                  <g fill="none" fill-rule="evenodd">
                    <rect
                      width="40"
                      height="26"
                      fill="url(#dLvChIa)"
                      rx="4"
                    ></rect>
                    <path
                      fill="#000"
                      fill-opacity=".101"
                      fill-rule="nonzero"
                      d="M4 .75A3.249 3.249 0 00.75 4.006v17.988A3.256 3.256 0 004 25.25h32a3.249 3.249 0 003.25-3.256V4.006A3.256 3.256 0 0036 .75H4zM4 0h32c2.204 0 4 1.793 4 4.006v17.988A3.999 3.999 0 0136 26H4c-2.204 0-4-1.793-4-4.006V4.006A3.999 3.999 0 014 0z"
                    ></path>
                    <g fill-rule="nonzero">
                      <path
                        fill="#231F20"
                        d="M11.272 21.892v-1.295a.768.768 0 00-.812-.82.799.799 0 00-.725.367.758.758 0 00-.682-.367.682.682 0 00-.604.306v-.254H8v2.063h.453v-1.135a.483.483 0 01.505-.548c.298 0 .45.194.45.544V21.9h.452v-1.144a.486.486 0 01.505-.548c.307 0 .454.194.454.544V21.9l.453-.009zm6.706-2.063h-.738v-.626h-.454v.626h-.41v.41h.419v.95c0 .479.186.764.717.764.198 0 .392-.055.56-.16l-.129-.384a.829.829 0 01-.397.116c-.216 0-.298-.138-.298-.345v-.941h.734l-.004-.41zm3.828-.052a.609.609 0 00-.543.302v-.25h-.445v2.063h.449v-1.157c0-.34.147-.53.432-.53a.732.732 0 01.28.051l.138-.432a.96.96 0 00-.32-.056l.01.009zm-5.788.216a1.543 1.543 0 00-.842-.216c-.522 0-.863.25-.863.66 0 .337.25.544.712.609l.216.03c.246.035.363.1.363.216 0 .16-.164.25-.47.25a1.099 1.099 0 01-.687-.215l-.216.35c.261.182.575.276.893.267.596 0 .941-.28.941-.673s-.271-.553-.72-.618l-.216-.03c-.194-.026-.35-.065-.35-.203s.147-.242.393-.242c.227.003.45.064.647.177l.199-.362zm12.024-.216a.609.609 0 00-.544.302v-.25h-.445v2.063h.45v-1.157c0-.34.146-.53.43-.53a.732.732 0 01.281.051l.139-.432a.96.96 0 00-.32-.056l.009.009zm-5.784 1.08a1.042 1.042 0 001.1 1.078c.27.014.535-.074.743-.246l-.216-.362a.906.906 0 01-.54.185.663.663 0 010-1.32.906.906 0 01.54.185l.216-.363a1.08 1.08 0 00-.743-.246 1.042 1.042 0 00-1.1 1.08v.008zm4.204 0v-1.028h-.45v.25a.783.783 0 00-.647-.302 1.08 1.08 0 000 2.158.783.783 0 00.648-.302v.25h.449v-1.027zm-1.67 0a.624.624 0 111.245.073.624.624 0 01-1.246-.074zm-5.418-1.08a1.08 1.08 0 00.03 2.158c.31.016.616-.084.857-.28l-.216-.333a.982.982 0 01-.6.216.572.572 0 01-.617-.505h1.532v-.173c0-.647-.401-1.079-.98-1.079l-.006-.004zm0 .401a.512.512 0 01.522.501h-1.079a.53.53 0 01.548-.5h.01zm11.247.682V19h-.432v1.08a.783.783 0 00-.647-.303 1.08 1.08 0 000 2.158.783.783 0 00.647-.302v.25h.432V20.86zm.749.732a.216.216 0 01.149.058.2.2 0 01-.067.332.203.203 0 01-.082.018.216.216 0 01-.194-.125.203.203 0 01.045-.225.216.216 0 01.155-.058h-.006zm0 .365a.153.153 0 00.112-.048.16.16 0 000-.215.16.16 0 00-.112-.048.162.162 0 00-.115.048.16.16 0 000 .215.16.16 0 00.052.035.16.16 0 00.07.013h-.007zm.013-.257c.02-.001.04.005.056.017.013.011.02.028.02.046a.052.052 0 01-.016.038.076.076 0 01-.045.02l.062.071h-.05l-.057-.071h-.02v.071h-.04v-.19l.09-.002zm-.048.037v.051h.048a.045.045 0 00.026 0 .022.022 0 000-.019.022.022 0 000-.02.045.045 0 00-.026 0l-.048-.012zm-2.374-.877a.624.624 0 111.245.074.624.624 0 01-1.245-.074zm-15.157 0V19.83h-.45v.25a.783.783 0 00-.647-.302 1.08 1.08 0 000 2.158.783.783 0 00.648-.302v.25h.449V20.86zm-1.67 0a.624.624 0 11.625.66.62.62 0 01-.63-.66h.004z"
                      ></path>
                      <path
                        fill="#EB001B"
                        d="M19.5 5.491v11.018A7.153 7.153 0 0115.112 18C11.184 18 8 14.866 8 11s3.184-7 7.112-7c1.656 0 3.18.557 4.388 1.491z"
                      ></path>
                      <path
                        fill="#F79E1B"
                        d="M19.5 5.491v11.018A7.153 7.153 0 0023.888 18C27.816 18 31 14.866 31 11s-3.184-7-7.112-7c-1.656 0-3.18.557-4.388 1.491z"
                      ></path>
                      <path
                        fill="#FF5F00"
                        d="M19.5 5.5C21.022 6.78 22 8.767 22 11s-.978 4.22-2.5 5.5C17.978 15.22 17 13.233 17 11s.978-4.22 2.5-5.5z"
                      ></path>
                    </g>
                  </g>
                </svg>
              </div>
              <div class="flex flex-column f5 dark-gray lh-copy">
                <span>This account is billed to</span>
                <span class="f4 fw6">{{paymentCard.brand.toUpperCase()}} card ending in {{paymentCard.last4}}</span>
              </div>
            </div>
            <div class="pv1">
              <button class="hk-button--danger mr2 ember-view" @click="removePayment">
                Remove credit card
              </button>
              <button
                @click="editPaymentCardAction"
                class="async-button default hk-button--secondary ember-view"
                type="submit"
              >
                Change credit card
              </button>
            </div>
          </div>

          <!---->
        </div>
      </div>
      </template>
      <!---->
      <div id="usage">
        <div class="table-responsive current-usage ember-view">
          <table class="table">
            <tbody>
              <tr>
                <td class="title">Current Usage</td>

                <td>{{this.$toPrice(usage)}}</td>

                <td class="text-right">
                  <a
                    href="/expense-bills/"
                    class="bn bg-none hk-link underline"
                    target="_blank"
                  >View Details</a>
                </td>
              </tr>

              <tr>
                <td class="title">Platform Credits</td>

                <td class="credits-remaining">{{this.$toPrice(amount)}}</td>

                <td class="text-right"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AccountBillingInformation from "./AccountBillingInformation";
export default AccountBillingInformation;
</script>

<style scoped>
</style>
