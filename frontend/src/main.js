// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import { store } from './store/store'
import axios from 'axios'

Vue.use(BootstrapVue);
Vue.config.productionTip = false;

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
// axios.defaults.headers.post['Authorization'] = 'Token ' + sessionStorage.getItem('auth_token');
// router.beforeEach((to, from, next) =>{
//   console.log('Before each');
//   next()
// });



new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});
