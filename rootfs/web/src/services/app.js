import axios from "../utils/axios";

export function getAPPList(clusterID, search='', limit=30, offset=0) {
    return axios.get(`/clusters/${clusterID}/apps/?limit=${limit}&offset=${offset}&search=${search}`)
}

export function dealAPPList(obj) {
    return obj.data.results.map(item => {
        return {
            id: item.id,
            name: item.id,
            owner: item.owner,
            created: item.created,
            updated: item.updated
        }
    })
}

export function deleteApp(clusterID, appId) {
    return axios.delete(`/clusters/${clusterID}/apps/${appId}/`)
}

export function createApp(clusterID, appId) {
    return axios.post(`/clusters/${clusterID}/apps/`, {id: appId})
}

export function updateApp(clusterID, appId, owner) {
    // Transfer Ownership
    return axios.post(`/clusters/${clusterID}/apps/${appId}/`, {owner: owner})
}
