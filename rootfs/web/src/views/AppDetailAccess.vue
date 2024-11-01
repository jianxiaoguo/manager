<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <access-collaborator-edit v-if="isShowEdit"
                        :editAccess="editAccess"
                        :appDetail="appDetail"
                        @closeEdit="closeEdit"
    />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box>
            <template v-slot:nav-cluster>
                <cluster-app-detail :app-detail="appDetail"/>
            </template>
            <template v-slot:navbox-extension>
                <nav-box-app-detail-menu :app-detail="appDetail"/>
            </template>
        </nav-box>
        <div class="main-content">
            <main-nav :is-access-active="true" :app-detail="appDetail"/>
            <div class="collaborator-list limit-width ember-view">
                <table class="w-100 mb5">
                    <thead>
                    <tr class="w-100 f5">
                        <th class="pl1 pr1 pv2 bb b--light-gray b" colspan="2">
                            Collaborators
                        </th>
                        <th class="pv2 pr1 bb b--light-gray b">
                            Role
                        </th>
                        <th class="pv2 bb b--light-gray b tr" style="width:138px;">
                            <button class="hk-button--secondary" @click="showEdit(null)">Add collaborator</button>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    <template v-for="access in accesses">
                        <tr class="collaborator-item ember-view">
                            <td class="bb b--light-silver pa2 dtc w--28">
                                <span style="width: 28px; height: 28px" class="gravatar-icon br-100 ember-view" data-original-title="" title="">
                                    <img :src="'/v1/avatar/' + access.username" >
                                </span>
                            </td>
                            <td class="w-40 bb b--light-silver pv2 pr1">{{access.username}}</td>
                            <td class="bb b--light-silver pv2 pr1">{{access.permissions}}</td>
                            <td class="bb b--light-silver tc ph2">
                                <button @click="showEdit(access)" class="bg-transparent hk-focus-ring--blue:focus cursor-hand br1 ba0 b--none pa--1 mr3" title="Edit" type="button">
                                    <span class="clip">Edit</span>
                                    <icon-edit-one theme="outline" size="20" fill="#333"/>
                                </button>
                            </td>
                        </tr>
                    </template>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AppDetailAccess from "./AppDetailAccess"
export default AppDetailAccess
</script>

<style scoped>

</style>
