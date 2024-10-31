<template>
  <div class="invoice-box">
    <table cellpadding="0" cellspacing="0">
      <tbody>
      <tr class="top">
        <td colspan="2">
          <table>
            <tbody>
            <tr>
              <td class="title">
                <img
                  src="https://www.drycc.cc/static/img/svg/logo.svg"
                  style="width: 100%; max-width: 300px"
                />
              </td>

              <td>
                Invoice #: {{invoice.period}}<br />
                From: {{fromDate}}<br />
                To: {{toDate}}
              </td>
            </tr>
            </tbody>
          </table>
        </td>
      </tr>

      <tr class="information">
        <td colspan="2">
          <table>
            <tbody>
            <tr>
              <td>
                {{fromCompany.name}}<br />
                {{fromCompany.address.line1}}<br />
                {{fromCompany.address.line2}}<br v-if="fromCompany.address.line2"/>
                {{fromCompany.address.city}}, {{fromCompany.address.state}} {{fromCompany.address.postcode}}<br />
                {{fromCompany.address.country}}
                <template v-if="consumer.provider.no">
                TAX №: {{consumer.provider.no}}<br />
                </template>
              </td>

              <td v-if="paymentCard != ''">
                <template v-if="address != ''">
                {{paymentCard.name}}<br />
                {{address.address1}}<br />
                {{address.address2}}<br v-if="address.address2"/>
                <template v-if="address.city">{{address.city}}, </template>{{address.state}} {{address.postcode}}<br />
                {{address.country}}<br />
                {{address.other}}<br v-if="address.other"/>
                </template>
                <template v-else>
                {{paymentCard.name}}<br />
                {{paymentCard.line1}}<br />
                {{paymentCard.line2}}<br v-if="paymentCard.line2"/>
                <template v-if="paymentCard.city">{{paymentCard.city}}, </template>{{paymentCard.state}} {{paymentCard.postcode}}<br />
                {{paymentCard.country}}<br />
                {{paymentCard.other}}<br v-if="paymentCard.other"/>
                </template>
                <template v-if="consumer.no">
                TAX №: {{consumer.no}}<br />
                </template>
              </td>
            </tr>
            </tbody>
          </table>
        </td>
      </tr>
      <tr class="heading" v-if="invoice.payment_methods.length > 0">
        <td>Payment Method</td>
        <td>Amount</td>
			</tr>
      <tr class="item" v-for="item in invoice.payment_methods" :key="item">
					<td>{{item.remark}}</td>
					<td>{{this.$toPrice(item.amount)}}</td>
			</tr>
      <tr class="details"><td></td><td></td></tr>
      <tr class="heading">
        <td>Description</td>
        <td>Price</td>
      </tr>
      
      <tr class="item" v-for="item in invoice.bill_summary" :key="item">
        <td>{{item.app_id}} * {{item.type}}</td>
        <td>{{this.$toPrice(item.price)}}</td>
      </tr>

      <tr class="summary">
        <td>Subtotal</td>
        <td>{{invoice.price > 0 ? this.$toPrice(invoice.price) : 0}}</td>
      </tr>

      <tr class="summary">
        <td>Discount</td>
        <td>- {{invoice.discount > 0 ? this.$toPrice(invoice.discount) : 0}}</td>
      </tr>
      <tr class="summary">
        <td>{{`Tax Due (${consumer.provider.rate}%)`}}</td>
        <td>+ {{invoice.tax > 0 ? this.$toPrice(invoice.tax) : 0}}</td>
      </tr>
  
      <tr class="total">
        <td>GRAND TOTAL</td>
        <td>{{invoice.total > 0 ? this.$toPrice(invoice.total) : 0}}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import AccountInvoiceDetail from "./AccountInvoiceDetail";
export default AccountInvoiceDetail;
</script>

<style scoped>
.invoice-box {
  max-width: 800px;
  margin: auto;
  padding: 30px;
  border: 1px solid #eee;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
  font-size: 16px;
  line-height: 24px;
  font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
  color: #555;
}

.invoice-box table {
  width: 100%;
  line-height: inherit;
  text-align: left;
}

.invoice-box table td {
  padding: 5px;
  vertical-align: top;
}

.invoice-box table tr td:nth-child(2) {
  text-align: right;
}

.invoice-box table tr.top table td {
  padding-bottom: 20px;
}

.invoice-box table tr.top table td.title {
  font-size: 45px;
  line-height: 45px;
  color: #333;
}

.invoice-box table tr.information table td {
  padding-bottom: 40px;
}

.invoice-box table tr.heading td {
  background: #eee;
  border-bottom: 1px solid #ddd;
  font-weight: bold;
}

.invoice-box table tr.details td {
  padding-bottom: 20px;
}

.invoice-box table tr.item td {
  border-bottom: 1px solid #eee;
}

.invoice-box table tr.item.last td {
  border-bottom: none;
}

.invoice-box table tr.summary td:nth-child(1) {
  float: right;
}

.invoice-box table tr.total {
  border-top: 2px solid #eee;
  font-weight: bold;
}

.invoice-box table tr.total td:nth-child(1) {
  float: right;
  margin-top: -1px;
}

@media only screen and (max-width: 600px) {
  .invoice-box table tr.top table td {
    width: 100%;
    display: block;
    text-align: center;
  }

  .invoice-box table tr.information table td {
    width: 100%;
    display: block;
    text-align: center;
  }
}

/** RTL **/
.invoice-box.rtl {
  direction: rtl;
  font-family: Tahoma, "Helvetica Neue", "Helvetica", Helvetica, Arial,
    sans-serif;
}

.invoice-box.rtl table {
  text-align: right;
}

.invoice-box.rtl table tr td:nth-child(2) {
  text-align: left;
}
</style>
