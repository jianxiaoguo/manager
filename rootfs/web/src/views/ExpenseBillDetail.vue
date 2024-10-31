<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box>
            <template v-slot:nav-cluster>
                <a href="/expense" class="link dark-gray active ember-view">Expense Bill</a>
            </template>
            <template v-slot:navbox-extension>

            </template>
        </nav-box>
        <div class="main-content">
            <nav class="account-nav nav nav-tabs sub-nav ember-view">
                <div class="limit-width">
                    <div class="sub-nav-item ember-view">
                        <a href="#" @click="goToExpenseBills" class="ember-view">
                            <span class="sub-nav-item-name gray">Summary</span>
                        </a>
                    </div>
                    <div class="account-application-nav sub-nav-item ember-view">
                        <a href="#" @click="goToExpenseBillsDetails" class="active ember-view">
                            <span class="sub-nav-item-name gray">Details</span>
                        </a>
                    </div>

                </div>
            </nav>

            <div class="w-100 flex limit-width">
                <el-row :gutter="20">
                    <el-col :span="6">
                        <el-select clearable class="purple" v-model="cluster" placeholder="Select Cluster">
                            <el-option
                            v-for="item in clusterOptions"
                            :key="item.code"
                            :label="item.name"
                            :value="item.uuid"
                            >
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="6">
                        <el-select
                            v-model="app"
                            filterable
                            remote
                            reserve-keyword
                            placeholder="Search keyword"
                            :disabled="cluster ===''"
                            :remote-method="filterAppOptions"
                        >
                            <el-option
                            v-for="item in appOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
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
            <div class="w-100 mt4 ml2 mb2 mr2 limit-width">
                <div class="w-100 ma2 flex-column">
                    <div class="collaborator-list limit-width ember-view">
                        <table class="w-100 mb5">
                            <thead>
                            <tr class="w-100 f5">
                                <th class="pl1 pr1 pv2 bb b--light-gray b">
                                    UUID
                                </th>
                                <th class="pl1 pr1 pv2 bb b--light-gray b">
                                    App ID
                                </th>
                                <th class="pv2 pr1 bb b--light-gray b">
                                    Type
                                </th>
                                <th class="pv2 pr1 bb b--light-gray b">
                                    Price
                                </th> 
                                <th class="pv2 pr1 bb b--light-gray b">
                                    Period
                                </th> 
                                <th class="pv2 pr1 bb b--light-gray b">
                                    Created
                                </th>
                                 <th class="pv2 pr1 bb b--light-gray b">
                                    Remark
                                </th> 
                            </tr>
                            </thead>
                            <tbody>
                            <tr class="ember-view"  v-for="bill in billList" :key="bill">
                                <td class="bb b--light-silver pv2 pl1 gray">{{bill.uuid}}</td>
                                <td class="bb b--light-silver pv2 pl1 gray">{{bill.app_id}}</td>
                                <td class="bb b--light-silver pv2 pl1 gray">{{bill.type}}</td>
                                <td class="bb b--light-silver pv2 pl1 gray">{{this.$toPrice(bill.price)}}</td>
                                <td class="bb b--light-silver pv2 pl1 gray">{{bill.period}}</td>
                                <td class="bb b--light-silver pv2 pl1 gray">{{bill.created}}</td>
                                <td class="bb b--light-silver pv2 pr1 gray">
                                    <el-tooltip
                                        v-if="bill.remark && bill.remark.length > 1"
                                        class="item"
                                        effect="dark"
                                        :content="bill.remark"
                                        :placement="more"
                                    >
                                    <icon-more>more</icon-more>
                                    </el-tooltip>
                                    <span v-else>{{bill.remark}}</span>
                                </td>
                            </tr>
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

        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import ExpenseBillDetail from  "./ExpenseBillDetail"
export default ExpenseBillDetail
</script>

<style scoped>

</style>
