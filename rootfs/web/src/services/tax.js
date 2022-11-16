import axios from "../utils/axios";

export function getConsumerTaxInfoTypes() {
    return axios.get(`/taxs/consumer-tax-info/types/`)
}

export function getConsumerTaxInfo() {
    return axios.get(`/taxs/consumer-tax-info/`)
}

export function addConsumerTaxInfo(data) {
    return axios.post(`/taxs/consumer-tax-info/`, data)
}

export function updateConsumerTaxInfo(data) {
    return axios.put(`/taxs/consumer-tax-info/`, data)
}
