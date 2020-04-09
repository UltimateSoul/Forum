<template>
  <div>
    <modal name="user-request-for-team">
      <div>
        <h1>
          Thank you!
        </h1>
        <h5>
          Captain of this team will consider your request soon!
        </h5>
        <b-button @click="hideUserRequestModal" variant="success">Ok</b-button>
      </div>
    </modal>
    <modal name="team-requests" :scrollable="true" height="auto" :draggable="true">
      <div v-for="request in teamRequests">
        <b-card
          :title="request.user.username"
          :img-src="request.user.avatar"
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 80rem;"
          class="mb-2"
        >
          <b-button variant="success" @click="patchRequest(true, request.id)">Accept Request</b-button>
          <b-button variant="danger" @click="patchRequest(false, request.id)">Reject Request</b-button>
        </b-card>
      </div>
    </modal>
    <b-row>
      <b-col lg="8">
        <b-button class="float-left" v-if="isOwner" @click="goToEditTeam"
                  variant="success">
          Edit Team
        </b-button>
      </b-col>
      <b-col lg="4">
        <b-button class="float-right" v-if="isOwner && teamRequests.length" @click="showTeamRequestModal"
                  variant="success">
          {{ teamRequestsButtonText }}
        </b-button>
        <b-button class="float-right" v-if="isOwner && !teamRequests.length" @click="showTeamRequestModal"
                  variant="success" disabled>
          {{ teamRequestsButtonText }}
        </b-button>
        <b-button class="float-right" v-if="!isMember && !isOwner && !requestForUserExists" @click="joinTeam"
                  variant="success">Join Team
        </b-button>
      </b-col>
    </b-row>
    <div>
      <img :src="team.avatar" height="250" width="250">
      <hr>
      <h1>
        {{ team.name }}
      </h1>
      <hr>
      <h5>
        {{ team.description }}
      </h5>
      <hr>
      <div @click="showTeamMembers = !showTeamMembers" class="clicable">
        <h3>Team Members:</h3>
      </div>
      <div v-show="showTeamMembers">
        <b-table striped hover :items="members" :fields="memberFields">
          <template v-slot:cell(avatar)="data">
            <img v-if="data.item.user.avatar" :src="data.item.user.avatar" height="100" width="100">
            <img v-else src="http://0.0.0.0:5000/static/images/default.jpg" height="100" width="100">
            <!--            ToDo: change in prod-->
          </template>
          <template v-slot:cell(username)="data">
            {{ data.item.user.username }}
          </template>
          <template v-slot:cell(game_nickname)="data">
            {{ data.item.user.game_nickname }}
          </template>
          <template v-slot:cell(rank)="data">
            <div v-if="data.item.rank">
              {{ data.item.rank.name }}
            </div>
          </template>
        </b-table>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {mapGetters} from 'vuex'

  export default {
    name: "Team",
    data() {
      return {
        team: {
          avatar: '',
          baseInfo: '',
          totalMembers: 0,
          createdAt: '',
          description: '',
          id: 0,
          name: '',
        },
        ranks: [],
        maxRanksNumber: 15,
        members: [],
        teamRequests: [],
        memberFields: ['avatar', 'username', 'game_nickname', 'rank'],
        owner: {},

        showTeamMembers: false,
        showTeamRequests: false,
        requestForUserExists: false,
      }
    },
    created() {
      const vueInstance = this;
      this.$store.dispatch('fetchUser');
      this.getData(this.$route.params.teamID).then(
        () => {
          if (vueInstance.isOwner) {
            vueInstance.getTeamRequests(1)
          } else {
            vueInstance.checkIfRequestExists(vueInstance.$route.params.teamID)
          }
        }
      );
      this.getTeamRanks(this.$route.params.teamID);
    },
    watch: {
      '$route'(to, from) {
        this.getData(to.params.teamID);
        this.getTeamRanks(to.params.teamID);
      }
    },
    methods: {
      getData(teamID) {
        return axios.get(`teams/${teamID}/`)
          .then(
            (response) => {
              switch (response.status) {
                case 200:
                  this.members = response.data.members;
                  this.owner = response.data.owner;
                  this.team.avatar = response.data.avatar;
                  this.team.baseInfo = response.data.base_info;
                  this.team.id = response.data.id;
                  this.team.name = response.data.name;
                  this.team.description = response.data.description;
                  this.team.createdAt = response.data.created_at;
                  this.team.totalMembers = response.data.total_members;
                  break;
                case 400:
                  break;
                case 404:
                  break;
                case 500:
                  break;

              }
            }
          )
      },
      patchRequest(isAccepted, requestID) {
        const data = {
          approved: isAccepted
        };
        return axios.patch(`user-team-requests/${requestID}/`, data)
      },
      getTeamRequests(page) {
        const data = {
          teamID: this.team.id,
          page: page
        };
        return axios.get('user-team-requests/get-requests-for-team/', {
          params: data
        }).then(
          (response) => {
            switch (response.status) {
              case 200:
                this.teamRequests = response.data.results;
                break;
              case 400:
                break;
              case 403:
                break;
            }
          }
        )
      },
      checkIfRequestExists(teamID) {
        return axios.get('user-team-requests/is-request-exist/', {
          params: {teamID: teamID}
        }).then(
          (response) => {
            switch (response.status) {
              case 200:
                this.requestForUserExists = true;
                break;
              case 404:
                this.requestForUserExists = false;
                break;
              default:
                this.requestForUserExists = false;
            }
          }
        )
      },
      getTeamRanks(teamID) {
        return axios.get('ranks/get_team_ranks/', {
          params:
            {teamID: teamID}
        }).then(
          (response) => {
            switch (response.status) {
              case 200:
                this.ranks = response.data;
                break;
              case 400:
                break;
            }
          }
        )
      },
      showUserRequestModal() {
        this.$modal.show('user-request-for-team')
      },
      hideUserRequestModal() {
        this.$modal.hide('user-request-for-team')
      },
      showTeamRequestModal() {
        this.$modal.show('team-requests')
      },
      hideTeamRequestModal() {
        this.$modal.hide('team-requests')
      },
      joinTeam() {
        const data = {
          team: this.$route.params.teamID
        };
        axios.post('user-team-requests/', data).then(
          (response) => {
            switch (response.status) {
              case 201:
                this.showUserRequestModal();
                break;
              case 222:
                break;
              case 403:
                console.log('Unauthorized or forbidden');
                break;
              case 400:
                break;
              default:
                console.log('default behaviour')
            }
          }
        )
      },
      goToEditTeam() {
        this.$router.push({
          'name': 'edit-team',
          params: {
            teamID: this.$route.params.teamID
          }
        })
      }
    },
    computed: {
      ...mapGetters([
        'getUserData',
        'isHasTeam'
      ]),
      isOwner() {
        return this.owner.pk === this.getUserData.userID
      },
      isMember() {
        const userID = this.getUserData.userID;
        // ToDo: figure out why doestn't work
        this.members.forEach(function (member) {
          return member.user.pk === userID
        });
        return false
      },
      teamRequestsButtonText() {
        if (this.teamRequests.length) {
          return 'Show Team Requests'
        } else {
          return 'No team requests'
        }
      }
    }
  }
</script>

<style scoped>

</style>
