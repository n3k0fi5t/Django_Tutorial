import axios from 'axios'
import Vue from 'vue'

Vue.prototype.$http = axios
// axios.defaults.baseURL = 'http://127.0.0.1:5001/api'
axios.defaults.baseURL = '/api'
// axios.defaults.baseURL = 'http://0.0.0.0:8081'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'
const getAPI = axios.create({
    baseURL: 'http://127.0.0.1:5001',
    timeout: 1000,
})

// const getAPI = ajax({
//     url: 'http://127.0.0.1:5001',
//     method: 'get'
// })

export default {
    getPostList (headers) {
        return ajax('/posts/', 'get', {
            headers
        })
    },
    createPost (headers, data) {
        return ajax('/posts/', 'post', {
            headers,
            data
        })
    },
    userLogin (data) {
        return ajax('/account/login/', 'post', {
            data
        })
    }
}

function ajax(url, method, options) {
    let default_headers = {'X-Requested-With': 'XMLHttpRequest'}
    if (options !== undefined) {
        var {params = {}, data = {}, headers = default_headers} = options
    } else {
        params = data = {}
        headers = default_headers
    }
    return new Promise((resolve, reject) => {
        axios({
            url,
            method,
            headers,
            params,
            data
        }).then(resp => {
            // if (resp.data.error !== null) {
            //     console.log(resp.data.error)
            //     reject(resp)
            // } else {
            //     resolve(resp)
            // }
            resolve(resp)
        }, resp => {
            reject(resp)
        })
    })
}

export { getAPI }