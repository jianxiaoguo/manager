import {reactive, toRefs, onMounted, ref} from 'vue'
import NavBar from "../components/NavBar.vue";
import NavBox from "../components/NavBox.vue";
import MainFooter from "../components/MainFooter.vue";
import ClusterAppDetail from "../components/ClusterAppDetail.vue";
import NavBoxAppDetailMenu from "../components/NavBoxAppDetailMenu.vue"
import MainNav from "../components/MainNav.vue";
import { Terminal } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import { WebLinksAddon } from '@xterm/addon-web-links'
import { useStore } from "vuex";

import '@xterm/xterm/css/xterm.css'

export default {
    name: "AppTerminal",
    components: {
        'nav-bar': NavBar,
        'nav-box': NavBox,
        'main-footer': MainFooter,
        'cluster-app-detail': ClusterAppDetail,
        'nav-box-app-detail-menu': NavBoxAppDetailMenu,
        'main-nav': MainNav,
    },
    setup() {
        const store = useStore()
        const state = reactive({
            loading: ref(true),
            appDetail: Object,
            terminal: Object,
            background: '#282c34',
        })

        onMounted(async () => {
            state.appDetail = store.getters.currentApp
            const channels = {stdin: String.fromCharCode(0), error: String.fromCharCode(3), resize: String.fromCharCode(4)};

            const fitAddon = new FitAddon()
            state.terminal = new Terminal({
                convertEol: true,
                cursorBlink: true,
                theme: {
                  background: state.background,
                  foreground: '#abb2bf',
                }
            })
            state.terminal.open(document.getElementById('terminal'))
            state.terminal.loadAddon(fitAddon)
            state.terminal.loadAddon(new WebLinksAddon())
            fitAddon.fit()
            //websocket
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const host = window.location.host;
            const path = `v1/clusters/${store.getters.currentCluster.uuid}/apps/${state.appDetail.id}/terminal/`
            const websocket = new WebSocket(`${protocol}/${host}/${path}`)

            websocket.onopen = function() {
                state.loading = false
            };

            websocket.onerror = function(event) {
                state.terminal.reset()
                state.terminal.write("The connection has been closed")
            };

            websocket.onclose = function(event) {
                state.terminal.reset()
                state.terminal.write("The connection has been closed")
            };

            state.terminal.onData((data) => {
                if (websocket.readyState === WebSocket.OPEN) {
                    websocket.send(channels.stdin + data)
                }
            });
        
            websocket.onmessage = (event) => {
                const data = event.data.slice(1)
                const channel = event.data.charAt(0)
                if (channel === channels.error) {
                    websocket.close()
                } else {
                    state.terminal.write(data)
                }
            };

            window.addEventListener('resize', () => {
                fitAddon.fit()
                if (websocket.readyState === WebSocket.OPEN) {
                    websocket.send(channels.resize + JSON.stringify({Height: terminal.rows, Width: terminal.cols}))
                }
            });
        })

        return {
            ...toRefs(state)
        }
    },
}
