import { createStore } from 'vuex'


export default createStore({
state: {
    user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : null,
    clusters: localStorage.getItem("clusters") ? JSON.parse(localStorage.getItem("clusters")) : [],
    currentCluster: localStorage.getItem("currentCluster") ? JSON.parse(localStorage.getItem("currentCluster")) : null,
    currentApp: localStorage.getItem("currentApp") ? JSON.parse(localStorage.getItem("currentApp")) : null,
    unreadMessageCount: 0,
},
mutations: {
    setUser(state, user) {
        state.user = user
        if (user) {
            localStorage.setItem("user", JSON.stringify(user))
        }
    },
    setClusters(state, clusters) {
        state.clusters = clusters
        if (clusters) {
            localStorage.setItem("clusters", JSON.stringify(clusters))
        }
    },
    setCurrentCluster(state, cluster) {
        state.currentCluster = cluster
        if (cluster) {
            localStorage.setItem("currentCluster", JSON.stringify(cluster))
        }
    },
    setCurrentApp(state, app) {
        state.currentApp = app
        if (app) {
            localStorage.setItem("currentApp", JSON.stringify(app))
        }
    },
    setUnreadMessageCount(state, count) {
        state.unreadMessageCount = count
    }
},
actions: {
    setUser({ commit }, user) {
        commit('setUser', user)
    },
    setClusters({ commit }, clusters) {
        commit('setClusters', clusters)
    },
    setCurrentCluster({ commit }, cluster) {
        commit('setCurrentCluster', cluster)
    },
    setCurrentApp({ commit }, app) {
        commit('setCurrentApp', app)
    },
    setUnreadMessageCount({ commit }, count) {
        commit('setUnreadMessageCount', count)
    }
},
getters: {
    user: state => state.user,
    clusters: state => state.clusters,
    currentCluster: state => state.currentCluster,
    currentApp: state => state.currentApp,
    unreadMessageCount: state => state.unreadMessageCount,
}
})
