import countries from '../data/countries.json'
import {onMounted, reactive, ref, toRefs, watch} from "vue";
import {getPaymentCard} from '../services/bill'
import { getConsumerTaxInfoTypes, getConsumerTaxInfo, addConsumerTaxInfo, updateConsumerTaxInfo} from '../services/tax'

export default {
    name: "AccountTaxInformation",
    setup() {
        const state = reactive({
            countries: countries,
            consumerTaxInfo :ref({
                no: "",
                type: 0,
                name: "",
                city: "",
                state: "",
                country: "",
                status: "",
            }),
            editEnabled: false,
            nullAddress: false,
            paymentCard: ref(""),
            consumerTaxInfoTypes: [],
        })

        const editEditConsumerTaxInfo = async () => {
            state.editEnabled = true;
        }

        const canelEditConsumerTaxInfo = async () => {
            await initData()
            state.editEnabled = false;
        }

        const saveConsumerTaxInfo = async () => {
            if(state.nullAddress) {
                await addConsumerTaxInfo(state.consumerTaxInfo)
                state.nullAddress = false;
            } else {
                await updateConsumerTaxInfo(state.consumerTaxInfo)
                state.nullAddress = false;
            }
            state.editEnabled = false;
        }

        const initData = async () => {
            state.useWatch = false
            let res = await getConsumerTaxInfo()
            if (Object.keys(res.data).length == 0) {
                state.nullAddress = true;
            }else{
                state.consumerTaxInfo = res.data;
            }
            state.useWatch = true

            res = await getPaymentCard()
            if(Object.keys(res.data).length != 0) {
                state.paymentCard = res.data
            }
            res = await getConsumerTaxInfoTypes()
            state.consumerTaxInfoTypes = res.data
        }

        onMounted(async () => { 
            await initData() 
        })

        return {
            ...toRefs(state),
            editEditConsumerTaxInfo,
            canelEditConsumerTaxInfo,
            saveConsumerTaxInfo,
        }
    }
}
