import axios from "../utils/axios";

export function getAppConfig(clusterID, appId, params='') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/config/` + '?' + params)
}

export function dealAppConfig(obj) {
    var appConfigs = []
    for (let key in obj.data.values) {
        appConfigs.push({"name": key, "value": obj.data.values[key]})
    }
    console.log("js appConfigs value: ", appConfigs)
    return appConfigs.map(item => {
        return {
            'name': item.name,
            'value': item.value,
            'isReadOnly': true
        }
    })

    // return obj.data.values
}

export function postAppConfigs(clusterID, appId, params) {
    let configs = {
        values: params
    }
    return axios.post(`/clusters/${clusterID}/apps/${appId}/config/`, configs)
}
