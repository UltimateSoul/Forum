// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import { store } from './store/store'

Vue.use(BootstrapVue);
Vue.config.productionTip = false;

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
