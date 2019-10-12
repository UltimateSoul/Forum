import axios from 'axios'

const state = {
  user: {
    isLogged: false,
    authToken: '',
    userID: null,
    username: '',
    email: '',
    bloodCoins: 0,
    avatarImage: '',
    gameNickName: '',
    city: '',
    gender: ''
  },
};

const getters = {
  isLogged(state) {
    state.isLogged = Boolean(sessionStorage.getItem('auth_token'));
    return state.user.isLogged;  // ToDo: now it does not check real availability of auth token, need to fix it
  },
  getUserData(state) {
    return state.user;
  }
};

const actions = {
  login(context, data) {
    return axios.post('http://127.0.0.1:8000/login/api-token-auth/', data)
      .then((response) => {
          sessionStorage.setItem('auth_token', response.data.token);
          context.commit('setAuthToken', response.data.token);
          context.dispatch('fetchUser', response.data.token)
        }
      )
  },
  fetchUser({commit}, authToken) {
    let data = {auth_token: authToken};
    return axios.get('/get-user/', {params: data})
      .then((response) => {
        debugger;
        let userData = response.data[0];
        commit('setUserData', userData)
      })
      .catch((error) => {
        console.log(error)
      })
  }
};

const mutations = {
  setAuthToken(state, authToken) {
    state.user.authToken = authToken
  },
  setUserData(state, userData) {
    let user = state.user;
    user.ID = userData.id;
    user.username = userData.username;
    user.email = userData.email;
    user.bloodCoins = userData.blood_coins;
    user.avatarImage = userData.avatar;
    user.city = userData.city;
    user.gender = userData.gender;
    user.gameNickName = userData.game_nickname;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
}
