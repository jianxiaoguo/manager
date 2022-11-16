import axios from "../utils/axios";

export function getBalance() {
    var url = `/funds/balance/`
    return axios.get(url)
}


export function getAccountFundingList(trading_type=null, direction=null, period=null, limit=30, offset=0) {
    var url = `/funds/flows/?`
    // var section=`2021-05-17%2006:01:46,2021-05-30%2006:01:48`
    // var section = null
    if (trading_type && trading_type !== '') {
        url += `trading_type=${trading_type}`
    }
    if (direction && direction !== '') {
        url += `&direction=${direction}`
    }
    if (period && period !== '') {
        url += `&period=${period}`
    }
    url += `&limit=${limit}&offset=${offset}`
    return axios.get(url)
}

export function dealAccountFundingList(obj) {
    return obj.data.results.map(item => {
        return {
            tradeNo: item.uuid,
            tradeTime: item.created,
            tradeType: item.trading_type,
            direction: item.direction,
            tradeAmount: item.amount,
            balance: item.balance,
            balance: item.balance,
            tradeNote: item.remark,
        }
    })
}
