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
    return state.user.isLogged;
  },
  getUserData(state) {
    let user = state.user;
    return {
      userID: user.userID,
      username: user.username,
      email: user.email,
      bloodCoins: user.bloodCoins,
      avatar: user.avatarImage,
      gameNickName: user.gameNickName,
      city: user.city,
      gender: user.gender
    };
  }
};

const actions = {
  login(context, data) {
    return axios.post('http://127.0.0.1:8000/login/api-token-auth/', data)  // ToDo: change URL in production
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
        let userData = response.data[0];
        commit('setUserData', userData)
      })
      .catch((error) => {
        console.log(error)
      })
  },
  register({commit}, registrationData) {
    return axios.post('/register/', registrationData, )
      .then()
  }
};

const mutations = {
  setAuthToken(state, authToken) {
    state.user.isLogged = Boolean(sessionStorage.getItem('auth_token'));
    state.user.authToken = authToken
  },
  setUserData(state, userData) {
    state.user.userID = userData.id;
    state.user.username = userData.username;
    state.user.email = userData.email;
    state.user.avatarImage = userData.avatar;
    state.user.city = userData.city;
    state.user.gender = userData.gender;
    state.user.gameNickName = userData.game_nickname;
  },
  logout(state) {
    sessionStorage.removeItem('auth_token');
    state.user.isLogged = false;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
}
