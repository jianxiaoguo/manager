import axios from "../utils/axios";

export function getChargeRules(cluster_id, types='', limit=30, offset=0) {
    var url = `/pricing/?cluster_id=${cluster_id}&limit=${limit}&offset=${offset}`
    if(types) {
        url &= `&types=${types}`
    }
    return axios.get(url)
}

export function calcCost(data){
    return axios.post(`/pricing/calc/`, data)
}