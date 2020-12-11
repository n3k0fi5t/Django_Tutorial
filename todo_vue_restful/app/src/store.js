import Vue from 'vue'
import { getAPI } from './axios-api'
import Vuex from 'vuex'

Vue.use(Vuex)
export default new Vuex.Store({
    state: {
        accessToken: null,
        refreshToken: null,
        islogin: false,
        sessionid: null,
        APIData: ''
    },
    mutations: {
        updateStorage (state, { access, refresh }) {
            state.accessToken = access
            state.refreshToken = refresh
        },
        destroyToken (state) {
            state.accessToken = null
            state.refreshToken = null
        },
        updateStatus (state, { status }) {
            state.islogin = status
        }
    },
    getters: {
        loggedIn (state) {
            return state.islogin != false
        }
    },
    actions: {
        // TODO: understand Promise resolve and reject meaning
        // and then
        userLogin (context, usercredentials) {
            return new Promise((resolve, reject) => {
                getAPI.post('/api-token-auth/', {
                    username: usercredentials.username,
                    password: usercredentials.password
                })
                .then(response => {
                    context.commit('updateStorage', {
                        access: response.data.token,
                        refresh: ""
                    })
                    resolve()
                })
                .catch(err => {
                    console.log(err)
                    reject()
                })
            })
        },
        login (context) {
            context.commit('updateStatus', {
                status: true
            })
        },
        userLogout (context) {
            if (context.getters.loggedIn) {
                context.commit('destroyToken')
            }
        }
    }
})