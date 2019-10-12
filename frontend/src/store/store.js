import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

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

  },
  mutations: {

  }
});
