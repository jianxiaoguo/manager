import axios from "../utils/axios";

export function getAppDomains(clusterID, appId, params='') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/domains/` + '?' + params)
}

export function dealAppDomains(obj) {
    return obj.data.results.map(item => {
        return {
            domain: item.domain,
        }
    })
}

export function addAppDomains(clusterID, appId, domain) {
    return axios.post(`/clusters/${clusterID}/apps/${appId}/domains/`, {domain: domain})
}

export function deleteAppDomains(clusterID, appId, domain) {
    return axios.delete(`/clusters/${clusterID}/apps/${appId}/domains/${domain}/`)
}
