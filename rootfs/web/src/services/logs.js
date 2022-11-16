import axios from "../utils/axios";

export function getApplogs(clusterID, appId, params='') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/logs` + '?' + params)
}

export function dealApplogs(obj) {
    return obj.data
}
