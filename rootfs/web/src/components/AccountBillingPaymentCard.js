import countries from '../data/countries.json'
import { loadStripe } from '@stripe/stripe-js';
import { ElMessage, ElLoading } from 'element-plus'
import { publicKey, setupIntent } from '../services/bill'
import { useStore } from "vuex";
import { onMounted, reactive, ref, toRefs } from "vue";

export default {
    name: "AccountBillingPaymentCard",
    props: {
        publicKey: ref(''),
    },
    setup(props, context) {
        const store = useStore()
        const state = reactive({
            countries: countries,
            billing_details: {
                address: {
                    city: ref(''),
                    country: ref(''),
                    line1: ref(''),
                    line2: ref(''),
                    postal_code: ref(''),
                    state: ref(''),
                },
                email: store.getters.user.email,
                name: ref(''),
            },
            card: ref(''),
            other: ref(''),
            stripe: ref(''),
        })

        const initStripe = async () => {
            const stripe = await loadStripe(props.publicKey)
            const elements = stripe.elements();

            const cardNumber = elements.create('cardNumber', { showIcon: true });
            cardNumber.mount('#card-number');
            const cardExpiry = elements.create('cardExpiry');
            cardExpiry.mount('#card-expiry');
            const cardCvc = elements.create('cardCvc');
            cardCvc.mount('#card-cvc');
            const postalCode = elements.create('postalCode');
            postalCode.mount('#card-postcode');
            
            state.card = cardNumber
            state.stripe = stripe

        }

        const closePaymentCard = async () => {
            context.emit('closePaymentCardAction', { "savePaymentCard": false })
        }

        const checkBillingDetails = () => {
            var errorMessage = ""
            if (state.billing_details.name === ""){
                errorMessage = "Full/Business Name is required."
            }
            else if(state.billing_details.address.country === ""){
                errorMessage = "Country is required."
            }
            else if(state.billing_details.address.line1 === ""){
                errorMessage = "Billing address line 1 is required."
            }
            else if(state.billing_details.address.city === ""){
                errorMessage = "City is required."
            }
            else if(state.billing_details.address.state === ""){
                errorMessage = "State/Province is required."
            }
            else if(state.billing_details.address.state === ""){
                errorMessage = "State/Province is required."
            }
            if(errorMessage != ""){
                ElMessage.error(errorMessage);
                return false
            }
            return true
        }

        const savePaymentCard = async () => {
            if(checkBillingDetails()){
                const loading = ElLoading.service()
                var res = await setupIntent()
                state.stripe.confirmCardSetup(res.data.client_secret, {
                    payment_method: {
                        card: state.card,
                        billing_details: state.billing_details,
                        metadata: {
                            other: state.other,
                        }
                    },
                }).then(function (result) {
                    loading.close()
                    if (result.error) {
                        ElMessage.error(`${result.error.param}: ${result.error.message}`);
                    } else {
                        context.emit('closePaymentCardAction', { "savePaymentCard": true })
                    }
                });
            }
        }

        onMounted(async () => {
            const loading = ElLoading.service()
            await initStripe()
            loading.close()
        })
        return {
            ...toRefs(state),
            savePaymentCard,
            closePaymentCard,
        }
    }
}
