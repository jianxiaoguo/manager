import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import AccountBillingInformation from "../components/AccountBillingInformation.vue";
import AccountInvoices from "../components/AccountInvoices.vue";
import AccountTaxInformation from "../components/AccountTaxInformation.vue";
import AccountInvoiceAddress from "../components/AccountInvoiceAddress.vue";
import MainFooter from "../components/MainFooter.vue";
import AccountSettingClose from "../components/AccountSettingClose.vue";
import { useRouter } from 'vue-router'

export default {
    name: "AccountBilling",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'account-billing-information': AccountBillingInformation,
        'account-invoices': AccountInvoices,
        'account-tax-information': AccountTaxInformation,
        'account-invoice-address': AccountInvoiceAddress,
        'account-setting-close': AccountSettingClose
    },
    setup(props) {
        const router = useRouter()

        const goToAccountSetting = () => {
            router.push({ path: `/account` })
        }

        const goToAccountFunding = () => {
            router.push({ path: `/account/funding` })
        }

        const goToAccountBilling = () => {
            router.push({ path: `/account/billing` })
        }

        return {
            // ...toRefs(state),
            goToAccountSetting,
            goToAccountFunding,
            goToAccountBilling
        }

    }
}
