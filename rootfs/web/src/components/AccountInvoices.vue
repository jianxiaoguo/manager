<template>
  <div class="panel-section">
    <div class="section-description">
      <div class="section-title f3 purple">Invoices</div>
    </div>

    <div v-if="lessInvoices.length > 0" class="panel-content">
      <div class="ember-view">
        <div class="table-responsive invoices">
          <table class="table">
            <tbody>
              <tr
                class="invoice-row ember-view"
                :key="invoice"
                v-for="invoice in showMore ? moreInvoices : lessInvoices"
              >
                <td class="invoice-title">
                  <a
                    :href="'/account/invoice/'+invoice.uuid+'/'"
                    target="_blank"
                    class="bn bg-none hk-link underline"
                  >{{getFormattedDate(invoice.period)}}</a>
                </td>

                <td class="invoice-total">{{ invoice.price }}</td>

                <td class="invoice-pay">
                  <!---->
                </td>
                <td
                  v-if="invoice.status === 'Unpaid'"
                  class="text-right invoice-state no-charge unpaid"
                >
                  {{ invoice.status }}
                </td>
                <td
                  v-else-if="invoice.status === 'Paid'"
                  class="text-right invoice-state no-charge paid"
                >
                  {{ invoice.status }}
                </td>
                <td v-else class="text-right invoice-state no-charge">
                  {{ invoice.status }}
                </td>
              </tr>
            </tbody>
          </table>

          <button
            v-if="moreInvoices.length > lessShowLine"
            class="btn btn-default btn-xs show-more"
            @click="showMoreInvoices"
          >
            {{ showMore == false ? "Show more" : "Show less" }}
          </button>
        </div>
      </div>
    </div>
    <div v-else class="panel-content">
      <div class="ember-view">
        <div class="hk-well ember-view">
          <div class="f3 dark-gray lh-title mv1 ember-view">
            There is no historical usage data to show yet
          </div>
          <div class="f5 gray lh-copy ember-view">
            Once you've been using Drycc for more than a month we'll be able to
            show you your monthly usage and invoice information.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AccountInvoices from "./AccountInvoices";
export default AccountInvoices;
</script>

<style scoped>
</style>
