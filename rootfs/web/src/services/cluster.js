import axios from '../utils/axios'


export async function getClusters() {
    const res = await axios.get('/clusters/')
    if(res.data) {
        const data = res.data.results.map(item => {
            return {
                uuid: item.uuid,
                name: item.name,
                code: item.name,
                url: item.url,
            }
        })
        return data
    }
}

export async function getCurrentCluster() {
    const clusters = await getClusters()
    const currentClusterJSON = localStorage.getItem("currentCluster")
    var currentCluster = clusters[0]
    if(currentClusterJSON) {
        const _currentCluster = JSON.parse(currentClusterJSON)
        for(let index in clusters){
            let cluster = clusters[index]
            if(cluster.code === _currentCluster.code){
                currentCluster = cluster
            }
        }
    }
    if(currentCluster){
        localStorage.setItem("currentCluster", JSON.stringify(currentCluster))
    }
    return currentCluster
}

export function setCurrentCluster(cluster) {
    if(cluster) {
        localStorage.setItem("currentCluster", JSON.stringify(cluster))
    }
}
