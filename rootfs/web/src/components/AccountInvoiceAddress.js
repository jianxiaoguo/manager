import countries from '../data/countries.json'
import {onMounted, reactive, ref, toRefs} from "vue";
import { getInvoiceAddress, addInvoiceAddress, updateInvoiceAddress, deleteInvoiceAddress, getPaymentCard} from '../services/bill'

export default {
    name: "AccountInvoices",
    setup() {
        const state = reactive({
            countries: countries,
            invoiceAddress :{
                country: "",
                state: "",
                city: "",
                postcode: "",
                address1: "",
                address2: "",
                other: "",
            },
            editEnabled: false,
            nullAddress: false,
            paymentCard: ref(""),
        })

        const editInvoiceAddress = async () => {
            state.editEnabled = true;
        }

        const canelEditInvoiceAddress = async () => {
            state.editEnabled = false;
        }

        const saveInvoiceAddress = async () => {
            if(state.nullAddress) {
                await addInvoiceAddress(state.invoiceAddress)
                state.nullAddress = false;
            } else {
                await updateInvoiceAddress(state.invoiceAddress)
                state.nullAddress = false;
            }
            state.editEnabled = false;
        }

        const removeInvoiceAddress = async () => {
            let res = await deleteInvoiceAddress()
            if (res.status == 204) {
                state.nullAddress = true;
                state.editEnabled = false;
            }
        }

        onMounted(async () => {
            let res = await getInvoiceAddress()
            if (Object.keys(res.data).length == 0) {
                state.nullAddress = true;
            }else{
                state.invoiceAddress = res.data;
            }
            res = await getPaymentCard()
            if(Object.keys(res.data).length != 0) {
                state.paymentCard = res.data
            }
        })
        return {
            ...toRefs(state),
            editInvoiceAddress,
            canelEditInvoiceAddress,
            saveInvoiceAddress,
            removeInvoiceAddress,
        }
    }
}
