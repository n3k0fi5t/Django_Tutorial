import 'babel-polyfill'
import Vue from 'vue'
import App from './App.vue'
import router from './router/index.js'
import store from './store/index.js'

import iView from 'iview'
import 'iview/dist/styles/iview.css'

import 'bootstrap/dist/css/bootstrap.min.css'


Vue.config.productionTip = false

Vue.use(iView)

// global message
Vue.prototype.$Message.config({
  duration: 2
})
Vue.prototype.$error = (s) => Vue.prototype.$Message.error(s)
Vue.prototype.$info = (s) => Vue.prototype.$Message.info(s)
Vue.prototype.$success = (s) => Vue.prototype.$Message.success(s)

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
