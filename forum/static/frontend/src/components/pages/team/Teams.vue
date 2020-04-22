<template>
  <div>
    <div>
      <modal name="notifications-modal" :clickToClose="false">
        <div class="m-5 text-center">
          <div v-for="notification in notifications">
            <h1>{{notification.type}} {{notification.status}}</h1>
            <h5>{{notification.message}}</h5>
          </div>
          <b-button @click="hideNotificationsEmail" variant="success">Ok</b-button>
        </div>
      </modal>
      <div class="button-control">
        <b-button v-if="!hasTeam" @click="goToCreateTeam" variant="outline-primary">Create Team</b-button>
        <b-button v-else variant="outline-primary" @click="goToMyTeam">Visit my team</b-button>
      </div>
      <b-table @row-clicked="clickTeam" striped hover :items="teams" :fields="fields">
        <template v-slot:cell(avatar)="data">
          <img :src="data.item.avatar" height="100" width="100">
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
        notifications: [],
        fields: ['avatar', 'name', 'owner', 'total_members', 'created_at'],
        teams: []
      }
    },
    created() {
      let vueInstance = this;
      this.$store.dispatch('fetchUser')
        .then(
          () => {
            vueInstance.getData();
          }
        );
    },
    methods: {
      getData() {

        return axios.get('teams/').then(
          (response) => {
            let notification = {}
            switch (response.status) {
              case 200:
                this.teams = response.data.results;
                break;
              case 204:
                notification = {
                  message: response.data,
                  type: 'error',
                  status: response.status
                }
                this.showNotificationsEmail()
                break;
            }
          }
        ).catch(
          (error) => {
            let notification = {}
            switch (error.response.status) {
              case 400:
                notification = {
                  message: error.response.data.detail,
                  type: 'error',
                  status: error.response.status
                }
                this.showNotificationsEmail()

                break;
              case 403:

                notification = {
                  message: error.response.data.detail,
                  type: 'error',
                  status: error.response.status
                }
                this.showNotificationsEmail()

                break
              case 500:
                notification = {
                  message: error.response.data.detail,
                  type: 'error',
                  status: error.response.status
                }
                this.showNotificationsEmail()
                break;
            }
            this.notifications.push(notification)
          }
        )
      },
      goToMyTeam() {
        this.$router.push({
          name: 'team',
          params: {
            teamID: this.getTeamID
          }
        })
      },
      showNotificationsEmail() {
        this.$modal.show('notifications-modal')
      },
      hideNotificationsEmail() {
        this.$modal.hide('notifications-modal')
        this.$router.push({name: 'home'});
      },
      goToCreateTeam() {
        this.$router.push({
          name: 'create-team'
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
        'getUserData',
        'hasTeam',
        'isTeamOwner',
        'getTeam',
        'getTeamID'
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
