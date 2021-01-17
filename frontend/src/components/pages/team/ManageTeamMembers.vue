<template>
  <div>
    <div>
      <h1> {{ team.name }} manage panel</h1>
    </div>
    <b-row>
      <modal name="editTeamMemberRankModal" height="auto">
        <div class="m-5 text-center" v-if="!loading">
          <h1>Choose rank for user {{ selectedUserName }}</h1>
          <div>
            <b-form-select v-model="selected" :options="ranks"></b-form-select>
          </div>
          <b-row>
            <b-col @click="hideEditTeamMemberRankModal">
              <b-button variant="dark">
                Cancel
              </b-button>
            </b-col>
            <b-col @click="saveUserRank">
              <b-button :disabled="selected" variant="success">
                Save
              </b-button>
            </b-col>
          </b-row>
        </div>
      </modal>
      <b-table striped hover :items="team.members" :fields="memberFields">
        <template v-slot:cell(avatar)="data">
          <img v-if="data.item.user.avatar" :src="data.item.user.avatar" height="100" width="100">
          <img v-else src="backend/static/images/default.jpg" height="100" width="100">
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
        <template v-slot:cell(options)="data">
          <b-col @click="showEditTeamMemberRankModal(data.item.user.username, data.item)">
            <edit-topic-button></edit-topic-button>
          </b-col>
          <b-col>
            <delete-topic-button></delete-topic-button>
          </b-col>
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
        ranks: [],
        selected: '',
        selectedUserName: '',
        selectedUserID: null,
      }
    },
    components: {
      DeleteTopicButton,
      EditTopicButton,
    },
    created() {
      this.$store.dispatch('getTeamData', this.$store.state.authentication.user.teamID).then(
        () => {
          if (!this.isTeamOwner) {
            this.$router.push({name: 'teams'})
          }
        }
      ).finally(
        () => {
          this.getTeamRanks()
        }
      )

    },
    methods: {
      getTeamRanks() {
        const data = {
          teamID: this.$store.state.authentication.user.teamID
        }
        axios.get('ranks/get-team-ranks/', {
          params: data
        }).then(
          (response) => {
            switch (response.status) {
              case 200:
                this.ranks = response.data
                this.ranks.forEach(
                  (rank, index) => {
                    this.ranks[index].text = rank.name
                  }
                )
                break;
            }
          }
        ).catch(
          (error) => {
            switch (error.response.status) {
              case 400:
                break;
              case 403:
                break;
              case 500:
                break;
            }
          }
        )
      },
      showEditTeamMemberRankModal(username, userID) {
        this.selectedUserName = username
        this.$modal.show('editTeamMemberRankModal')
      },
      hideEditTeamMemberRankModal() {
        this.selectedUserName = ''
        this.$modal.hide('editTeamMemberRankModal')
      },
      saveUserRank() {

      }
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
