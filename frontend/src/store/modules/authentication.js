import axios from 'axios'

const state = {
  user: {
    isLogged: false,
    userID: null,
    username: '',
    email: '',
    coins: 0,
    avatarImage: '',
    gameNickName: '',
    gender: '',
    date_joined: null,
    isModerator: false,
    isAdmin: false,
    hasTeam: false,
    isTeamOwner: false,
    teamID: null
  },
};

const getters = {
  isLogged(state) {
    return state.user.isLogged;
  },
  getTeamID(state) {
    return state.user.teamID
  },
  isModerator(state) {
    return state.user.isModerator
  },

  getUserData(state) {
    let user = state.user;
    return {
      userID: user.userID,
      username: user.username,
      dateJoined: user.dateJoined,
      email: user.email,
      coins: user.coins,
      avatar: user.avatarImage,
      gameNickName: user.gameNickName,
      gender: user.gender,
      hasTeam: user.hasTeam,
      teamID: user.teamID,
      isModerator: user.isModerator,
      isTeamOwner: user.isTeamOwner,
    };
  },
  isMainUser: state => idToCheck => {
    return state.user.userID === idToCheck;
  },

};

const actions = {
  login(context, data) {
    return axios.post('http://0.0.0.0:5000/authentication/api-token-auth/', data)  // ToDo: change URL in production
      .then((response) => {
          localStorage.setItem('auth_token', response.data.token);
          context.commit('setAuthToken');
          context.dispatch('fetchUser')
        }
      )
  },
  fetchUser({commit}) {
    return axios.get('/users/get-user/')
      .then((response) => {
        let userData = response.data;
        commit('setUserData', userData)
      })
      .catch((error) => {
        console.log(error)
      })
  },
  register(context, registrationData) {
    return axios.post('http://0.0.0.0:5000/authentication/register/', registrationData,)
      .then((response) => {
        let auth_token = response.data.auth_token;
        localStorage.setItem('auth_token', auth_token);
        context.commit('setAuthToken');
        context.dispatch('fetchUser')
      })
  }
};

const mutations = {
  setAuthToken(state) {
    state.user.isLogged = Boolean(localStorage.getItem('auth_token'));
    axios.defaults.headers.post['Authorization'] = 'Token ' + localStorage.getItem('auth_token');
    axios.defaults.headers.get['Authorization'] = 'Token ' + localStorage.getItem('auth_token');
    axios.defaults.headers.delete['Authorization'] = 'Token ' + localStorage.getItem('auth_token');
    axios.defaults.headers.patch['Authorization'] = 'Token ' + localStorage.getItem('auth_token');
  },
  setUserData(state, userData) {
    state.user.userID = userData.pk;
    state.user.username = userData.username;
    state.user.email = userData.email;
    state.user.avatarImage = userData.avatar;
    state.user.gender = userData.gender;
    state.user.gameNickName = userData.game_nickname;
    state.user.dateJoined = new Date(userData.date_joined);
    state.user.hasTeam = userData.has_team;
    state.user.teamID = userData.team_id;
    state.user.isTeamOwner = userData.is_team_owner;
    state.user.isModerator = userData.is_moderator;
  },
  logout(state) {
    localStorage.removeItem('auth_token');
    state.user.isLogged = false;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
}
