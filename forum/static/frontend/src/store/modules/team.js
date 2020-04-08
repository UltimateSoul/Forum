import axios from 'axios'

const state = {

};

const getters = {
  isHasTeam(state, getters, rootState) {
    return rootState.authentication.user.hasTeam;
  },
  isTeamOwner: (state, getters, rootState) => (teamID) => {
    return rootState.authentication.user.teamID === teamID
  }
};

const actions = {

};

const mutations = {
};

export default {
  state,
  getters,
  actions,
  mutations
}
