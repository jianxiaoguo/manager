<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box>
            <template v-slot:nav-cluster>
                <a href="/account" class="link dark-gray active ember-view">Manage Account</a>
            </template>
            <template v-slot:navbox-extension>

            </template>
        </nav-box>
        <div class="main-content">
            <nav class="account-nav nav nav-tabs sub-nav ember-view">
                <div class="limit-width">
                    <div class="sub-nav-item ember-view">
                        <a href="#" @click="goToAccountSetting" class="ember-view">
                            <span class="sub-nav-item-name gray">Account</span>
                        </a>
                    </div>
                    <div class="account-application-nav sub-nav-item ember-view">
                        <a href="#" @click="goToAccountFunding" class="active ember-view">
                            <span class="sub-nav-item-name gray">Funding</span>
                        </a>
                    </div>
                    <div class="sub-nav-item ember-view">
                        <a href="#" @click="goToAccountBilling" class="ember-view">
                            <span class="sub-nav-item-name gray">Billing</span>
                        </a>
                    </div>
                </div>
            </nav>

            <div class="collaborator-list limit-width ember-view">
                <div class="w-100 mb5">
                    <el-row :gutter="20">
                        <el-col :span="6">
                            <el-select clearable class="purple" v-model="direction" placeholder="Direction">
                                <el-option
                                v-for="item in directionOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                                >
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="6">
                            <el-select clearable class="purple" v-model="tradingType" placeholder="Trading Type">
                                <el-option
                                v-for="item in tradingTypeOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                                >
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="6">
                            <el-date-picker
                                v-model="period"
                                type="month"
                                placeholder="Period"
                            >
                            </el-date-picker>
                        </el-col>
                    </el-row>
                </div>
                <table class="w-100 mb5">
                    <thead>
                    <tr class="w-100 f5">
                        <th class="pl1 pr1 pv2 bb b--light-gray b">
                            trade no
                        </th>
                        <th class="pv2 pr1 bb b--light-gray b">
                            trade time
                        </th>
                        <th class="pv2 pr1 bb b--light-gray b">
                            trade type
                        </th>
                        <th class="pv2 pr1 bb b--light-gray b">
                            direction
                        </th>
                        <th class="pv2 pr1 bb b--light-gray b">
                            amount
                        </th>
                        <th class="pv2 pr1 bb b--light-gray b">
                            balance
                        </th>
                        <th class="pv2 pr1 bb b--light-gray b">
                            remark
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    <template v-for="funding in fundingList">
                        <tr class="ember-view">
                            <td class="bb b--light-silver pv2 pr1 gray">{{funding.tradeNo}}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{funding.tradeTime}}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{funding.tradeType}}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{funding.direction}}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{funding.tradeType===1 ? '+' + funding.tradeAmount : '-' + funding.tradeAmount}}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{funding.balance}}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">
                                <el-tooltip
                                    v-if="funding.tradeNote.length > 15"
                                    class="item"
                                    effect="dark"
                                    :content="funding.tradeNote"
                                >
                                <icon-more>more</icon-more>
                                </el-tooltip>
                                <span v-else>{{funding.tradeNote}}</span>
                            </td>
                        </tr>
                    </template>
                </tbody> 
                </table>
                <div class="limit-width bg-white mt4 pager">
                    <el-pagination
                    layout="prev, pager, next"
                    :page-size="pageSize"
                    :current-page="page"
                    :hide-on-single-page="true"
                    @current-change="pageCurrentChange"
                    :total="count">
                    </el-pagination>
                </div>
                
            </div>

        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AccountFunding from "./AccountFunding"
export default AccountFunding
</script>

<style scoped>

</style>
