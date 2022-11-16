import axios from "../utils/axios";

export function getBills(cluster_id=null, app_id=null, period=null, limit=30, offset=0) {
    var url = `/bills/?limit=${limit}&offset=${offset}`
    if(cluster_id && cluster_id !== ''){
        url += `&cluster_id=${cluster_id}`
    }
    if(app_id){
        url += `&app_id=${app_id}`
    }
    if(period){
        url += `&period=${period}`
    }
    return axios.get(url)
}

export function getBillsSummary(cluster_id=null, app_id=null, period=null, values=null, limit=30, offset=0) {
    var url = `/bills_summary/?limit=${limit}&offset=${offset}`
    if(cluster_id && cluster_id !== ''){
        url += `&cluster_id=${cluster_id}`
    }
    if(app_id){
        url += `&app_id=${app_id}`
    }
    if(period){
        url += `&period=${period}`
    }
    if(values){
        url += `&values=${values}`
    }
    return axios.get(url)
}

export function getInvoice(id) {
    var url = `/account/invoices/${id}/`
    return axios.get(url)
}

export function getInvoices(limit=30, offset=0) {
    var url = `/account/invoices?limit=${limit}&offset=${offset}`
    return axios.get(url)
}

export function getPaymentCard() {
    return axios.get(`/account/my_payment_card/`)
}

export function removePaymentCard() {
    return axios.delete(`/account/my_payment_card/`)
}

export function getInvoiceAddress() {
    return axios.get(`/account/my_invoice_address/`)
}

export function addInvoiceAddress(data) {
    return axios.post(`/account/my_invoice_address/`, data)
}

export function updateInvoiceAddress(data) {
    return axios.put(`/account/my_invoice_address/`, data)
}


export function deleteInvoiceAddress() {
    return axios.delete(`/account/my_invoice_address/`)
}

export function publicKey() {
    return axios.get(`/payments/stripe/public-key/`)
}

export function setupIntent() {
    return axios.post(`/payments/stripe/setup-intent/`)
}