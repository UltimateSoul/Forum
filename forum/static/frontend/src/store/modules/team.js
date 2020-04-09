import axios from 'axios'

const state = {
    id: null,
    totalMembers: 0,
    owner: {
      avatar: '',
      username: '',
      gameNickname: '',
      pk: null
    },
    members: [],
    name: '',
    description: '',
    baseInfo: '',
    avatar: '',
    createdDate: '',
};

const getters = {
  isHasTeam(state, getters, rootState) {
    return rootState.authentication.user.hasTeam;
  },
  isTeamOwner: (state, getters, rootState) => (teamID) => {
    return rootState.authentication.user.isTeamOwner && rootState.authentication.user.teamID === +teamID
  },
  getTeam(state) {
    return state
  },
  getTeamDescription(state) {
    return state.description
  },
  getTeamAvatar(state) {
    return state.avatar
  },
  getTeamName(state) {
    return state.name
  }
};

const actions = {
  getTeamData({commit, state}, teamID) {
    return axios.get(`teams/${teamID}/`).then(
      (response) => {
        switch (response.status) {
          case 200:
            commit('setTeamData', response.data)
        }
      }
    )
  }
};

const mutations = {
  setTeamData(state, teamData) {
    state.id = teamData.id
    state.totalMembers = teamData.total_members
    state.owner.avatar = teamData.owner.avatar
    state.owner.username = teamData.owner.username
    state.owner.gameNickname = teamData.owner.game_nickname
    state.owner.pk = teamData.owner.pk
    state.members = teamData.members
    state.name = teamData.name
    state.description = teamData.description
    state.baseInfo = teamData.base_info
    state.avatar = teamData.avatar
    state.createdDate = teamData.created_at
  }
};

export default {
  state,
  getters,
  actions,
  mutations
}
