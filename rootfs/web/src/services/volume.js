import axios from "../utils/axios";


export function getVolumes(clusterID, appId, params='') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/volumes/` + '?' + params)
}

export function dealVolumes(data) {
    data.data.results.forEach(item=> {
        var mountPoints = []
        Object.keys(item.path).forEach(key => {
            mountPoints.push(key + ":" + item.path[key])
        })
        item.path = mountPoints.join(",")
    })
    return data.data.results
}