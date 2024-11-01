import axios from "../utils/axios";

export function getAppAccesses(clusterID, appId, params='') {
    return axios.get(`/clusters/${clusterID}/apps/${appId}/perms/` + '?' + params)
}

export function addAppAccesses(clusterID, appId, username, permissions) {
    return axios.post(
        `/clusters/${clusterID}/apps/${appId}/perms/`,
        {username: username, permissions: permissions.toString()}
    )
}

export function updateAppAccesses(clusterID, appId, username, permissions) {
    return axios.put(
        `/clusters/${clusterID}/apps/${appId}/perms/${username}/`,
        {username: username, permissions: permissions.toString()}
    )
}

export function deleteAppAccesses(clusterID, appId, username) {
    return axios.delete(`/clusters/${clusterID}/apps/${appId}/perms/${username}/`)
}
