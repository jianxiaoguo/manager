import axios from "../utils/axios";

export function getAppAddons(clusterID, appId, params='') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/resources/` + '?' + params)
}

export function dealAppAddons(obj) {
    return obj.data.results.map(item => {
        return {
            name: item.name,
            plan: item.plan,
            status: item.status,
            
        }
    })
}

export function getServices(clusterID, limit=100, offset=0) {
    return axios.get(`/clusters/${clusterID}/resources/services/?limit=${limit}&offset=${offset}`)
}

export function getPlans(clusterID, serviceName, limit=100, offset=0) {
    return axios.get(`/clusters/${clusterID}/resources/services/${serviceName}/plans/?limit=${limit}&offset=${offset}`)
}