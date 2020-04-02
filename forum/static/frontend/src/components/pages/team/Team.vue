<template>
  <div>
    <div>
      <h1>
        My Team
      </h1>
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
        owner: {}
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
                this.ranks = response.data.ranks;
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
      ])
    }
  }
</script>

<style scoped>

</style>
