import types from '../types.js'
import storage from '@/utils/storage.js'
import {STORAGE_KEY} from '@/utils/constants.js'
import api from '@/axios-api.js'

export default {
    state: {
        profile: {}
    },
    getters: {
        user: state => state.profile.user || {},
        profile: state => state.profile,
        isAuthenticated: (state, getters) => {
            return !!getters.user.id
        }
    },
    mutations: {
        [types.CHANGE_PROFILE] (state, {profile}) {
            state.profile = profile
            storage.set(STORAGE_KEY.AUTHED, !!profile.user)
        }
    },
    actions: {
        getProfile ({commit}) {
            api.getUserInfo().then(res => {
                commit(types.CHANGE_PROFILE, {
                    profile: res.data.data || {}
                })
            }, err => {
                console.log(err)
            })
        },
        clearProfile ({commit}) {
            commit(types.CHANGE_PROFILE, {
                profile: {}
            })
            storage.clear()
        }
    }
}