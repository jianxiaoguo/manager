import axios from "../utils/axios";

export function getMetricStatus(clusterID, appId, containerType, interval){
    
    var end = parseInt(new Date().getTime()/1000)
    var start = end - (3600 * interval) + 60
    var every = (3600 * interval) / (60 * 60)
    every = every > 1 ? parseInt(every) : 1
    var url = `/clusters/${clusterID}/apps/${appId}/metrics/${containerType}/status/`
    url += `?start=${start}&stop=${end}&every=${every}m`
    return axios.get(url)
}
