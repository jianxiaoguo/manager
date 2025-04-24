<template>
    <div :id="'vue-content-'+Math.random().toString(36).substring(2)">
        <nav-bar />
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
                <main-nav :is-terminal-active="true" :app-detail="appDetail"/>
                <div v-loading="loading" class="limit-width ember-view b--silver">
                    <div id="terminal"></div>
                </div>
            </div>
        </div>
        <main-footer />
    </div>
    </template>
    
    <script>
    import AppTerminal from  "./AppTerminal"
    export default AppTerminal
    </script>
    
    <style scoped>
    #terminal {
        background-color: v-bind(background);
        padding: .4rem 0rem .4rem .4rem;
    }
    </style>