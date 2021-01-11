import Vue from 'vue'
import Vuex from 'vuex'
import types from './types.js'
import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        user
    },
    state: {
        modalStatus: {
            mode: 'login', // or register
            visible: false
        },
        website: {
            title: 'Online Memo'
        },
        redirect_path: '/'
    },
    getters: {
        modalStatus (state) {
            return state.modalStatus
        },
        website (state) {
            return state.website
        },
        redirect_path (state) {
            return state.redirect_path
        }
    },
    mutations: {
        [types.CHANGE_MODAL_STATUS] (state, {mode, visible}) {
            if (mode !== undefined) {
                state.modalStatus.mode = mode
            }
            if (visible !== undefined) {
                state.modalStatus.visible = visible
            }
        },
        [types.UPDATE_WEBSITE_CONF] (state, payload) {
            state.website = payload.websiteConfig
        },
        [types.UPDATE_REDIRECT_PATH] (state, path) {
            state.redirect_path = path
        }
    },
    actions: {
        changeModalStatus (context, payload) {
            context.commit(types.CHANGE_MODAL_STATUS, payload)
        },
        changeWebsiteConfig (context, payload) {
            if (payload)
                this.state.website = payload
        },
        changeDomTitle ({state}, payload) {
            if (payload && payload.title) {
              window.document.title = payload.title
            } else {
              window.document.title = state.route.meta.title
            }
          }
    },
})

export {types}