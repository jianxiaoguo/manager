import axios from "../utils/axios";

export function getAppProcesses(clusterID, appId) {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/`)

    // return new Promise((resolve, reject) => {
    //     let res = axios.get(`/clusters/${clusterID}/apps/${appId}/`)
    //     var procfile_structures = [];
    //     res.then(function (value) {
    //         for (var i in value.procfile_structure) {
    //             procfile_structures.push({"name": i, "cmd": value.procfile_structure[i], 'status': 1})
    //         }
    //         console.log("js getAppProcesses value: ", value)
    //         resolve(procfile_structures);
    //     }, function (err) {
    //         reject(err);
    //     })
    // });

    // return [
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '1'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '2'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '3'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '4'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '5'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '6'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '7'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '8'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '9'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '10'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '11'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '12'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '13'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '14'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:80', 'status': 1, 'id': '15'},
    //     {'name': 'web', 'cmd': 'python manage.py runserver 0.0.0.0:8000', 'status': 0, 'id': '16'}
    // ]
}

export function dealAppProcesses(obj) {
    var appProcesses = []
    for (let key in obj.data.procfile_structure) {
        appProcesses.push({
            "name": key,
            "cmd": obj.data.procfile_structure[key],
            'replicas': obj.data.structure[key]
        })
    }
    console.log("js appProcesses value: ", appProcesses)
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
    for (let i in obj.data.procfile_structure) {
        appProcessTypes.push({"name": i})
    }
    console.log("js appProcessTypes value: ", appProcessTypes)
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
