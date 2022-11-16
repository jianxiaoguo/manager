import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import AccountSettingProfile from "../components/AccountSettingProfile.vue";
import AccountSettingClose from "../components/AccountSettingClose.vue";
import { useRouter } from 'vue-router'

export default {
    name: "AccountSetting",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'account-setting-profile': AccountSettingProfile,
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
