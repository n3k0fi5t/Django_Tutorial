import axios from 'axios'
import Vue from 'vue'

import store from '@/store'

Vue.prototype.$http = axios
axios.defaults.baseURL = '/api'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
    getTodoList (offset, limit) {
        let params = {
            offset,
            limit,
        }
        return ajax('items/', 'get', {
            params
        })
    },
    updateItem(params, data) {
        return ajax('items/', 'put', {
            params,
            data
        })
    },
    getUserInfo () {
        return ajax('profile/', 'get')
    },
    login (data) {
        return ajax('login/', 'post', {
            data
        })
    },
    logout () {
        return ajax('logout/', 'get')
    },
    register (data) {
        return ajax('register/', 'post', {
            data
        })
    },
    checkUsernameOrEmail (username, email) {
        return ajax('check_username_or_email/', 'post', {
            data: {
                username,
                email
            }
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
    console.log(params)
    return new Promise((resolve, reject) => {
        axios({
            url,
            method,
            headers,
            params,
            data
        }).then(res => {
            resolve(res)
        }, error => {
            if (error.response && error.response.status === 401) {
                // clear profile and pop up login form
                Vue.prototype.$error("Please login first")
                store.dispatch('clearProfile')
                store.dispatch('changeModalStatus', {
                    mode: 'login',
                    visible: true
                })
            }
            reject(error)
        })
    })
}