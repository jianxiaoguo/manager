import { createStore } from 'vuex'


export default createStore({
    state: {
        user: '' || localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : '',
        clusters: localStorage.getItem("clusters") ? JSON.parse(localStorage.getItem("clusters")) : '',
        currentCluster: localStorage.getItem("currentCluster") ? JSON.parse(localStorage.getItem("currentCluster")) : '',
        currentApp: '' || localStorage.getItem("currentApp") ? JSON.parse(localStorage.getItem("currentApp")) : '',
        unreadMessageCount: 0,
    },
    mutations: {
        setUser(state, user) {
            state.user = user
            if(user){
                localStorage.setItem("user", JSON.stringify(user))
            }
        },
        setClusters(state, clusters) {
            state.clusters = clusters
            if(clusters){
                localStorage.setItem("clusters", JSON.stringify(clusters))
            }
        },
        setCurrentCluster(state, cluster) {
            state.currentCluster = cluster
            if(cluster) {
                localStorage.setItem("currentCluster", JSON.stringify(cluster))
            }
        },
        setCurrentApp(state, app) {
            state.currentApp = app
            if(app) {
                localStorage.setItem("currentApp", JSON.stringify(app))
            }
        },
        setUnreadMessageCount(state, count) {
            state.unreadMessageCount = count
        }
    },
    actions: {
        setUser(context, user) {
            context.commit('setUser', user)
        },
        setClusters(context, clusters) {
            context.commit('setClusters', clusters)
        },
        setCurrentCluster(context, cluster) {
            context.commit('setCurrentCluster', cluster)
        },
        setCurrentApp(context, app) {
            context.commit('setCurrentApp', app)
        },
        setUnreadMessageCount(context, count) {
            context.commit('setUnreadMessageCount', count)
        }
    },
    getters: {
        user : state => {
            return state.user
        },
        clusters : state => {
            return state.clusters
        },
        currentCluster : state => {
            return state.currentCluster
        },
        currentApp: state => {
            return state.currentApp
        },
        unreadMessageCount: state => {
            return state.unreadMessageCount
        }
    }
})
