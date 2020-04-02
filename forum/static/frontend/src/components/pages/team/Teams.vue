<template>
  <div>
    <div>
      <div class="button-control">
        <b-button v-if="!hasTeam" variant="outline-primary">Create Team</b-button>
        <b-button v-else variant="outline-primary" @click="goToMyTeam">Visit my team</b-button>
      </div>
      <b-table @row-clicked="clickTeam" striped hover :items="teams" :fields="fields">
        <template v-slot:cell(avatar)="data">
        <img :src="data.item.avatar" height="100" width="100">
          {{ data.avatar }}
        </template>
        <template v-slot:cell(owner)="data">
          {{ data.item.owner.username }}
        </template>
        <template v-slot:cell(created_at)="data">
          {{ data.item.created_at | getDateFormat }}
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {mapGetters} from 'vuex';

  export default {
    name: "Teams",
    data() {
      return {
        hasTeam: false,
        myTeamID: null,
        fields: ['avatar', 'name', 'owner', 'total_members', 'created_at'],
        teams: []
      }
    },
    created() {
      this.getData();
      this.isHasTeam();
    },
    methods: {
      getData() {
        return axios.get('teams/').then(
          (response) => {
            switch (response.status) {
              case 200:
                this.teams = response.data.results;
                break;
              case 204:
                break;
              case 400:
                break;
              case 500:
                break;
            }
          }
        ).catch(
          (error) => {
          }
        )
      },
      isHasTeam() {
        return axios.get('teams/is_has_team/').then(
          (response) => {
            this.hasTeam = Boolean(response.data.team_id);
            if (this.hasTeam) {
              this.myTeamID = response.data.team_id
            }
          }
        )
      },
      goToMyTeam() {
        this.$router.push({
          name: 'team',
          params: {
            teamID: this.myTeamID
          }
        })
      },
      clickTeam(rowData) {
        this.$router.push({
          name: 'team',
          params: {
            teamID: rowData.id
          }
        })
      }
    },
    computed: {
      ...mapGetters([
        'isMainUser',
        'getUserData'
      ]),
    },
    filters: {
      getDateFormat(value) {
        let date = new Date(value);
        return date.toLocaleDateString()
      }
    }
  }
</script>

<style scoped>

</style>
