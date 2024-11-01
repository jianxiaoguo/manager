import axios from "../utils/axios";

export function getCollaboratorActivities(clusterID, appId, params='limit=30') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/releases/` + '?' + params).then(function (response) {
        var results = {}
        response.data.results.forEach(item => {
            if(item["owner"] in results){
                results[item["owner"]] += 1
            } else {
                results[item["owner"]] = 1
            }
        });
        return results
    })
}

export function dealCollaboratorActivities(obj) {
    var results = []
    for(var key in obj){
        results.push({
            "username": key,
            "count": obj[key]
        })
    }
    return results
}

export function getAppActivities(clusterID, appId, params='limit=15') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/releases/` + '?' + params)
}

export function dealAppActivities(obj) {
    return obj.data.results.map(item => {
        return {
            content: item.summary,
            username: item.owner,
            version: item.version,
            failed: item.failed,
            deployed_ptypes: item.deployed_ptypes,
            created_time: item.created
        }
    })
}


export function postAppActivitieRollback(clusterID, appId, version) {
    return axios.post(`/clusters/${clusterID}/apps/${appId}/releases/rollback/`, {'version': version})
}
