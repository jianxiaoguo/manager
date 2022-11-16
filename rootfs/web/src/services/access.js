import axios from "../utils/axios";

export function getAppAccesses(clusterID, appId, params='') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/perms/` + '?' + params)
}

export function dealAppAccesses(app, obj) {
    var results = obj.data.users.map(item => {
        return {
            username: item,
            role: 'collaborator',
        }
    })
    results.push({username: app.owner, role: 'owner'})
    return results
}

export function addAppAccesses(clusterID, appId, username) {
    return axios.post(`/clusters/${clusterID}/apps/${appId}/perms/`, {username: username})
}

export function deleteAppAccesses(clusterID, appId, username) {
    return axios.delete(`/clusters/${clusterID}/apps/${appId}/perms/${username}/`)
}
