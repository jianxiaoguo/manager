<template>
<div id="main-content">
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative">
        <nav-box>
            <template v-slot:nav-cluster>
              <div>
                <a href="/notifications" class="link dark-gray active ember-view">Notifications--></a>
                <el-dropdown @command="unreadChange" class="ml1 mt1">
                  <span class="link dark-gray active ember-view">
                    {{unread === '' ? 'All messages' : unread === 'true' ? 'Unread message' : 'Read message' }}
                    <icon-down class="icon malibu-icon mr2" fill="#409EFF"/>
                  </span>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item :command="''">All messages</el-dropdown-item>
                      <el-dropdown-item :command="'false'">Read message</el-dropdown-item>
                      <el-dropdown-item :command="'true'">Unread message</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </template>
            <template v-slot:navbox-extension>
              <div>
                <button @click="markCurrentPageAsRead" :class="unreadMessageCount > 0 ? 'hk-button--secondary' : 'hk-button--disabled-secondary'" class="async-button default  ember-view" type="submit">
                  Mark current page as read
                </button>
              </div>
            </template>
        </nav-box>
    </div>
  <div class="main-panel bg-lightest-silver relative">
    <div class="main-content">
      <div v-if="messages.length == 0"  class="list-group notification-list limit-width">
        <p> You have no notifications at this time. </p>
      </div>

      <div v-if="messages.length > 0" class="collaborator-list limit-width ember-view">
        <table class="w-100 mb5">
          <tr class="w-100 f5">
            <th class="pv2 pr1 bb b--light-gray b">Sender</th>
            <th class="pv2 pr1 bb b--light-gray b">Message</th>
            <th class="pv2 pr1 bb b--light-gray b">Created</th>
            <th class="pv2 pr1 bb b--light-gray b">Type</th>
            <th class="pv2 pr1 bb b--light-gray b">Read</th>
            <th class="pv2 pr1 bb b--light-gray b">Action</th>
          </tr>
          <template v-for="message in messages">
            <tr class="collaborator-item ember-view" :class="message.unread ? 'dark-gray': 'gray'">
              <td @click="openMessage(message)" class="w-20 bb b--light-silver pv2 pr1">{{message.sender}}</td>
              <td @click="openMessage(message)" class="w-40 bb b--light-silver pv2 pr1">{{message.body.length > 20 ? message.body.slice(0, 20) + ' ...': message.body}}</td>
              <td @click="openMessage(message)" class="w-20 bb b--light-silver pv2 pr1">{{message.created}}</td>
              <td @click="openMessage(message)" class="w-10 bb b--light-silver pv2 pr1">{{message.type}}</td>
              <td @click="openMessage(message)" class="w-5 bb b--light-silver pv2 pr1">{{!message.unread}}</td>
              <td class="w-5 bb b--light-silver pv2 pr1"><icon-delete @click="deleteMessage(message)" class="ml3" /></td>
            </tr>      
          </template>
        </table>
      </div>
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
  <div>
    <el-drawer
      v-model="showMessageDetail"
      :with-header="false"
      direction="rtl"
    >
      <span>{{messageDetail}}</span>
    </el-drawer>
  </div>
  <main-footer />
</div>
</template>

<script>
import AccountNotifications from "./AccountNotifications"
export default AccountNotifications
</script>

<style scoped>

</style>
