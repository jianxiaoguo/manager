import axios from "../utils/axios";

export function getUser() {
    return axios.get(`/auth/whoami/`)
}

export function dealUser(obj) {
    return {
        username: obj.data.username,
        email: obj.data.email,
        first_name:  obj.data.first_name,
        last_name:  obj.data.last_name,
    }
}

export function getCsrf() {
    return axios.get('/auth/csrf/')
}

export function postLogout() {
    //axios.post(`/disconnect/drycc/`)
    return axios.post(`/logout/`)
}

export function getMessages(unread, limit=30, offset=0) {
    return axios.get(`/messages/` + `?limit=${limit}&offset=${offset}&unread=${unread}`)
}

export function deleteMessage(uuid) {
    return axios.delete(`/messages/${uuid}/`)
}

export function markAsReadMessage(uuid) {
    return axios.put(`/messages/${uuid}/`, {
        unread: false,
    })
}
