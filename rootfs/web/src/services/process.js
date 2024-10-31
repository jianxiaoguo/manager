import axios from "../utils/axios";

export function getAppProcesses(clusterID, appId) {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/`)
}

export function dealAppProcesses(obj) {
    var appProcesses = []
    for (let key in obj.data.structure) {
        var cmd = key in obj.data.structure ? obj.data.structure[key] : "undefined"
        appProcesses.push({"name": key, "cmd": cmd, "replicas": obj.data.structure[key]})
    }
    return appProcesses.map(item => {
        return {
            'name': item.name,
            'cmd': item.cmd,
            'replicas': item.replicas
        }
    })
}

export function getAppProcessTypes(clusterID, appId) {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/`)
    // return [
    //     {'name': 'web'}, {'name': 'celery'}, {'name': 'cbeat'}, {'name': 'cron'}, {'name': 'sync1'}, {'name': 'sync2'}
    // ]
}

export function dealProcessTypes(obj) {
    var appProcessTypes = []
    for (let i in obj.data.structure) {
        appProcessTypes.push({"name": i})
    }
    return appProcessTypes
}

export function getPsList(clusterID, appId){
    return axios.get(`/clusters/${clusterID}/apps/${appId}/pods/`)
}

export function dealPsList(obj) {
    var  processes = obj.data.results
    var pts = []

    for (let index in processes) {
        let exists = false
        // Is processtype for process already exists, append to it.
        for (let i in pts) {
            if (pts[i].type == processes[index].type) {
                exists = true
                if (processes[index].name != "") {
                    pts[i]['podsList'].push(pts[i].podsList, processes[index])
                }
                break
            }
        }
        // Is processtype for process doesn't exist, create a new one
        if (!exists) {
            let p = []
            let status = "started"
            if (processes[index].state == "stopped" && processes[index].replicas != "0") {
                status = "stopped"
            }
            if (processes[index].name == "") {
                p = []
            }
            pts.push({
                type:     processes[index].type,
                podsList: p,
                replicas: processes[index].replicas,
                status:   status,
            })
        }
    }

    // Sort the pods alphabetically by name.
    for (let i in pts) {
        pts[i].podsList.sort()
    }
    // Sort ProcessTypes alphabetically by process name
    pts.sort()
    return pts
}
