<template>
  <div>
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
              <img  v-else src="http://0.0.0.0:5000/static/images/default.jpg" height="100" width="100">
<!--            ToDo: change in prod-->
          </template>
          <template v-slot:cell(username)="data">
            {{ data.item.user.username }}
          </template>
          <template v-slot:cell(game_nickname)="data">
            {{ data.item.user.game_nickname }}
          </template>
          <template v-slot:cell(rank)="data">
            {{ data.item.rank.name }}
          </template>
        </b-table>
      </div>


    </div>
    <div class="button-control" v-if="isOwner">
      <b-button variant="outline-primary">Edit</b-button>
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
          totalMembers: 0,
          createdAt: '',
          description: '',
          id: 0,
          name: '',
        },
        ranks: [],
        maxRanksNumber: 15,
        members: [],
        memberFields: ['avatar', 'username', 'game_nickname', 'rank'],
        owner: {},
        showTeamMembers: false,
      }
    },
    created() {
      this.getData(this.$route.params.teamID);
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
      }
    },
    computed: {
      ...mapGetters([
        'getUserData'
      ]),
      isOwner() {
        return this.owner.pk === this.getUserData.userID
      }
    }
  }
</script>

<style scoped>

</style>
