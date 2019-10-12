import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios'
import VueAxios from 'vue-axios'
import {mapMutations, mapGetters} from 'vuex';
Vue.use(VueAxios, axios);
Vue.use(Vuex);
const SERVER_URL = '';

export const store = new Vuex.Store({
  state: {
    isLogged: false
  },
  getters: {
    isLogged(state) {
      state.isLogged = Boolean(sessionStorage.getItem('auth_token'));
      return state.isLogged;
    }
  },
  actions: {
    getSectionData(section) {

    }
  },
  mutations: {

  }
});
