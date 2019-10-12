import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'
import VueAxios from 'vue-axios'
import {mapMutations, mapGetters} from 'vuex';
import authentication from './modules/authentication'
Vue.use(VueAxios, axios);
Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {

  },
  getters: {

  },
  actions: {
    getSectionData(context, data) {
        return Vue.axios.get('topics/', {params: data});
    }
  },
  mutations: {

  },
  modules: {
    authentication
  }
});
