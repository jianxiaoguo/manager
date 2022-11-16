<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
  <nav-bar />
  <div class="main-panel bg-lightest-silver relative">
    <nav-box>
      <template v-slot:nav-cluster>
        <a href="/account" class="link dark-gray active ember-view">Application Logs</a>
      </template>
      <template v-slot:navbox-extension>
      </template>
    </nav-box>
  </div>

  <div class="build-view limit-width">
    <div class="flex justify-between">
      <div class="actions-button formation-filter-drop-down btn-group ember-view">
      </div>
    </div>
    <div class="build-stream build-stream-full ember-view"><div class="build-stream-output">
      <!---->
      <template v-for="log in logs">
        <pre class="build-stream-line"><span class="log-color log-color--blue">{{ log }}</span></pre>
      </template>

    </div>

      <footer class="build-stream-footer">
        <a class="hk-link" @click="saveLogs" href="#" data-ember-action="" data-ember-action-844="844">Save</a>
      </footer>
    </div>
  </div>
  <main-footer />
</div>
</template>

<script>
import AppDetailLogs from  "./AppDetailLogs"
export default AppDetailLogs
</script>

<style scoped>

</style>
