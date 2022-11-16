import axios from "../utils/axios";

export function getExpenseBillList(resource_type=null, section=null, params='limit=45&offset=0') {
    var url = `/bills/?`
    // var section=`2021-05-17%2006:01:46,2021-05-30%2006:01:48`
    if (resource_type && resource_type != 0) {
        url += `resource_type=${resource_type}`
    }
    if (section) {
        url += `&section=${section}`
    }
    if(params){
        url = url + '&' + params
    }
    return axios.get(url)
    // return [
    //     {'username': 'hanlucen', 'period': '2021-01', 'cost': 11021, 'app': {'app_id': '1', 'name': 'zmy1'}, 'product': {'name': 'cpu', 'detail': 'xxxx'}, 'start': 1611590400, 'end': 1611676800},
    //     {'username': 'hanlucen', 'period': '2021-01', 'cost': 1024, 'app': {'app_id': '1', 'name': 'zmy2'}, 'product': {'name': 'cpu', 'detail': 'xxxx'}, 'start': 1611590400, 'end': 1611676800},
    //     {'username': 'hanlucen', 'period': '2021-01', 'cost': 14401, 'app': {'app_id': '1', 'name': 'zmy3'}, 'product': {'name': 'cpu', 'detail': 'xxxx'}, 'start': 1611590400, 'end': 1611676800},
    //     {'username': 'hanlucen', 'period': '2021-01', 'cost': 4401, 'app': {'app_id': '1', 'name': 'zmy4'}, 'product': {'name': 'cpu', 'detail': 'xxxx'}, 'start': 1611590400, 'end': 1611676800},
    //     {'username': 'hanlucen', 'period': '2021-01', 'cost': 1401, 'app': {'app_id': '1', 'name': 'zmy5'}, 'product': {'name': 'cpu', 'detail': 'xxxx'}, 'start': 1611590400, 'end': 1611676800},
    //     {'username': 'hanlucen', 'period': '2021-01', 'cost': 101, 'app': {'app_id': '1', 'name': 'zmy6'}, 'product': {'name': 'cpu', 'detail': 'xxxx'}, 'start': 1611590400, 'end': 1611676800},
    // ]
}

export function dealExpenseBillList(obj) {
    var resource_types = {1:'Cpu',2:'Memory',3:'Volume',4:'Network'}
    return obj.data.results.map(item => {
        var resource_type = resource_types[item.resource_type]
        return {
            'period': item.created,
            'appCluser': item.cluster,
            'appName': item.app_id,
            'appContainer': eval('(' + item.resource_info + ')').container_type,
            'productName': resource_type,
            // 'productDetail': resource_type,
            'cost': item.sum_price,
            'start': item.start_time,
            'end': item.end_time,
        }
    })
}
