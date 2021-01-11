import Vue from 'vue'
import VueRouter from 'vue-router'

import routes from './routes'
import {sync} from 'vuex-router-sync'
import store from '../store'
import {STORAGE_KEY} from '@/utils/constants'
import storage from '../utils/storage'
import {types} from '@/store'

//next you need to call Vue.use(Router) to make sure that Router is added.
Vue.use(VueRouter)

const router = new VueRouter({
    //default mode for Vue Router is hash mode.
    //It uses a URL hash to simulate a full URL so that the page won't be reloaded when the URL changes.
    mode: 'history',
    routes
})

router.beforeEach((to, from, next) => {
    Vue.prototype.$Loading.start()

    //stop redirect
    if (from.path === to.path && from.query === to.query) {
        next(false)
    }

    if (to.matched.some(record => record.meta.requiresAuth)) {
        // route if does not authenticated yet
        if (!storage.get(STORAGE_KEY.AUTHED)) {
            Vue.prototype.$error('Please login first')
            store.commit(types.CHANGE_MODAL_STATUS, {mode: 'login', visible: true})
            store.commit(types.UPDATE_REDIRECT_PATH, to.path)
            next({
                name: 'home'
            })
        } else {
        next()
        }
    } else {
        next()
    }
})

// loading progress bar
router.afterEach((to, from, next) => {
    Vue.prototype.$Loading.finish()
})

sync(store, router)

export default router