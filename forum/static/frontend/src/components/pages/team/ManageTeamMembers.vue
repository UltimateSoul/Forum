<template>
  <div>
    <div>
      <h1> {{ team.name }} manage panel</h1>
    </div>
    <b-row>
      <b-table striped hover :items="team.members" :fields="memberFields">
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
          <template v-slot:cell(options)="row">
            <b-col> <edit-topic-button></edit-topic-button></b-col>
            <b-col><delete-topic-button></delete-topic-button></b-col>
          </template>
        </b-table>
    </b-row>
  </div>
</template>

<script>
  import DeleteTopicButton from '../../SVG/DeleteTopicButton'
  import EditTopicButton from '../../SVG/EditTopicButton'
  import axios from 'axios'
  import {mapGetters} from 'vuex'

  export default {
    name: "ManageTeamMembers",
    data() {
      return {
        loading: false,
        memberFields: ['avatar', 'username', 'game_nickname', 'rank', 'options'],
      }
    },
    components: {
      DeleteTopicButton,
      EditTopicButton,
    },
    created() {
      this.$store.dispatch('getTeamData', this.$store.state.authentication.user.teamID)
      if (!this.isTeamOwner) {
        this.$router.push({name: 'teams'})
      }
    },
    methods: {

    },
    computed: {
      ...mapGetters({
        team: 'getTeam',
        user: 'getUserData',
        isTeamOwner: 'isTeamOwner',

      })
    }
  }
</script>

<style scoped>

</style>
