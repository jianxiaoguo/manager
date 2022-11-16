import { createRouter, createWebHistory } from 'vue-router'
import AppList from "../views/AppList.vue";
import NewApp from "../views/NewApp.vue";
import AppDetailOverview from "../views/AppDetailOverview.vue";
import AppDetailAccess from "../views/AppDetailAccess.vue";
import AppDetailActivity from "../views/AppDetailActivity.vue";
import AppDetailDeploy from "../views/AppDetailDeploy.vue";
import AppDetailMetrics from "../views/AppDetailMetrics.vue";
import AppDetailResources from "../views/AppDetailResources.vue";
import AppDetailSettings from "../views/AppDetailSettings.vue";
import AppDetailLogs from "../views/AppDetailLogs.vue";
import AccountSetting from "../views/AccountSetting.vue";
import AccountFunding from "../views/AccountFunding.vue";
import AccountBilling from "../views/AccountBilling.vue";
import AccountInvoiceDetail from "../views/AccountInvoiceDetail.vue";
import AccountNotifications from "../views/AccountNotifications.vue"
import ExpenseBill from "../views/ExpenseBill.vue";
import ExpenseBillDetail from "../views/ExpenseBillDetail.vue";
import Pricing from "../views/Pricing.vue";

const routes = [
    {
        path: '/',
        redirect: '/apps',
    },
    {
        path: '/apps',
        name: 'Apps',
        component: AppList
    },
    {
        path: '/new-app',
        name: 'NewApp',
        component: NewApp
    },
    {
        path: '/apps/:id',
        name: 'AppDetailOverview',
        component: AppDetailOverview
    },
    {
        path: '/apps/:id/resources',
        name: 'AppDetailResources',
        component: AppDetailResources
    },
    {
        path: '/apps/:id/deploy/:deployType',
        name: 'AppDetailDeployDetail',
        component: AppDetailDeploy
    },
    {
        path: '/apps/:id/deploy',
        name: 'AppDetailDeploy',
        component: AppDetailDeploy
    },
    {
        path: '/apps/:id/metrics',
        name: 'AppDetailMetrics',
        component: AppDetailMetrics
    },
    {
        path: '/apps/:id/metrics/processes/:processType',
        name: 'AppDetailMetricsDetail',
        component: AppDetailMetrics
    },
    {
        path: '/apps/:id/activity',
        name: 'AppDetailActivity',
        component: AppDetailActivity
    },
    {
        path: '/apps/:id/access',
        name: 'AppDetailAccess',
        component: AppDetailAccess
    },
    {
        path: '/apps/:id/settings',
        name: 'AppDetailSettings',
        component: AppDetailSettings
    },
    {
        path: '/apps/:id/logs',
        name: 'AppDetailLogs',
        component: AppDetailLogs
    },
    {
        path: '/account',
        name: 'AccountSetting',
        component: AccountSetting
    },
    {
        path: '/account/funding',
        name: 'AccountFunding',
        component: AccountFunding
    },
    {
        path: '/account/billing',
        name: 'AccountBilling',
        component: AccountBilling
    },
    {
        path: '/account/invoice/:id',
        name: 'AccountInvoiceDetail',
        component: AccountInvoiceDetail
    },
    {
        path: '/expense-bills/details',
        name: 'ExpenseBillDetail',
        component: ExpenseBillDetail
    },
    {
        path: '/expense-bills',
        name: 'ExpenseBill',
        component: ExpenseBill
    },
    {
        path: '/notifications',
        name: 'AccountNotifications',
        component: AccountNotifications
    },
    {
        path: '/pricing',
        name: 'Pricing',
        component: Pricing
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach(function(to, from, next) {
    if (!router.store.getters.currentCluster) {
        if (to.path !== '/apps') {
            return next('/apps')
        }
    }else if(!router.store.getters.currentApp){
        var reg = /^\/apps\/[a-z]([a-z0-9-]*[a-z0-9])+$/
        if (reg.test(to.path)) {
            return next('/apps')
        }
    }
    next()
})

export default router
