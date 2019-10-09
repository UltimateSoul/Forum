// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
Vue.use(BootstrapVue);
Vue.config.productionTip = false;

// Vue.use({
//     install (Vue) {
//     Vue.prototype.$api = axios.create({
//       baseURL: 'http://localhost:8000/api/v1/'
//     })
//   }
// });

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});
