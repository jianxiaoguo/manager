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

export function dealMetricCpus(res){
    if(res.data && res.data.status && res.data.status.cpus){
        return [{
            name: 'MAX TOTAL',
            data: res.data.status.cpus.max.map(item => {
                let t = item[0] * 1000
                return [t, item[1]]
            }),            
        },
        {
            name: 'AVG TOTAL',
            data: res.data.status.cpus.avg.map(item => {
                let t = item[0] * 1000
                return [t, item[1]]
            }),            
        }]
    }else{
        return [{
            name: 'MAX TOTAL',
            data: [],            
        },
        {
            name: 'AVG TOTAL',
            data: [],            
        }]
    }
}
export function dealMetricMemory(res){
    if(res.data && res.data.status && res.data.status.memory){
        return [{
            name: 'MAX TOTAL',
            data: res.data.status.memory.max.map(item => {
                let t = item[0] * 1000
                return [t, item[1]]
            }),            
        },
        {
            name: 'AVG TOTAL',
            data: res.data.status.memory.avg.map(item => {
                let t = item[0] * 1000
                return [t, item[1]]
            }),            
        }]
    }else{
        return [{
            name: 'MAX TOTAL',
            data: [],            
        },
        {
            name: 'AVG TOTAL',
            data: [],            
        }]
    }
}
export function dealMetricNetworks(res){
    if(res.data && res.data.status && res.data.status.networks){
        let recv = []
        let send = []
        let total = []
        for(let index in res.data.status.networks){
            let item = res.data.status.networks[index]
            recv.push([item[0] * 1000, item[1]])
            send.push([item[0] * 1000, item[2]])
            total.push([item[0] * 1000, item[1]+item[2]])
        }
        return [{
            name: 'TOTAL',
            data: total,            
        },
        {
            name: 'RECEIVED',
            data: recv,            
        },
        {
            name: 'SENT',
            data: send,
        }]
    }else{
        return [{
            name: 'TOTAL',
            data:[],    
        },
        {
            name: 'RECEIVED',
            data:[],    
        },
        {
            name: 'SENT',
            data: [],    
        }]
    }
}