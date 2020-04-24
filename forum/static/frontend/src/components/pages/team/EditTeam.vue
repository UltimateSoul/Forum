<template>
  <div>
    <hr>
    <b-img height="250" width="250" :src="getTeamAvatar"></b-img>
    <hr>
    <h1>{{ getTeamName }} Team Editing</h1>
    <div class="form-container">
      <b-form>
        <b-form-group label="Quick description of your team" label-for="teamDescriptionInput">
          <b-form-input
            id="teamDescriptionInput"
            v-model="description"
            placeholder="Enter something..."
            :maxlength="255"
          ></b-form-input>
          <small id="teamDescriptionHelp" class="form-text text-muted">
            Here you can write something to introduce your team to other users.
          </small>
        </b-form-group>
        <hr>
        <b-form-group label="Base information about your team" label-for="teamBaseInfo">
          <ckeditor :editor="editor"
                    class="ck-content"
                    v-model="baseInfo"
                    :config="editorConfig">
          </ckeditor>
          <small id="teamBaseInfoHelp" class="form-text text-muted">
            Here you can write team rules, awards etc.
          </small>
        </b-form-group>
        <hr>
        <b-form-group label="Team Image" label-for="teamAvatarInput">
          <b-form-file
            id="teamAvatarInput"
            v-model="file"
            :state="Boolean(file)"
            placeholder="Choose an image file or drop it here..."
            drop-placeholder="Drop file here..."
          ></b-form-file>
          <small id="teamAvatarHelp" class="form-text text-muted">
            Add image that associates with your team.
          </small>
        </b-form-group>
        <hr>
        <div>
          <h1 id="ranks">Ranks</h1>
          <b-tooltip target="ranks">Your team ranks</b-tooltip>
          <div v-if="ranks.length">
            <b-table striped hover :items="ranks" :fields="rankFields">
              <template v-slot:cell(index)="data">
                {{ data.index + 1 }}
              </template>
              <template v-slot:cell(options)="row">
                <b-col>
                  <edit-topic-button id="edit-button"></edit-topic-button>
                  <b-tooltip target="edit-button">Edit this rank</b-tooltip>
                </b-col>
                <b-col>
                  <delete-topic-button id="delete-button"></delete-topic-button>
                  <b-tooltip target="delete-button">Delete this rank</b-tooltip>
                </b-col>
              </template>
            </b-table>
          </div>
          <div>
            <b-form>
              <b-form-group
                id="input-group-1"
                label="Rank name:"
                label-for="rank-input-name"
                description="Rank"
              >
                <b-form-input
                  id="rank-input-name"
                  v-model="rankInput.name"
                  type="text"
                  required
                  placeholder="Enter rank name"
                ></b-form-input>
              </b-form-group>
              <b-form-group
                id="input-group-2"
                label="Rank description:"
                label-for="rank-input-description"
                description="Rank"
              >
                <b-form-input
                  id="rank-input-description"
                  v-model="rankInput.description"
                  type="text"
                  required
                  placeholder="Enter rank description"
                ></b-form-input>
              </b-form-group>
              <b-button variant="dark" @click="addRank">Add Rank</b-button>
            </b-form>
          </div>
        </div>
        <hr>
        <div class="button-control">
          <button type="button"
                  class="btn btn-primary btn-lg"
                  @click="updateTeam"
          >Update
          </button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
  import DeleteTopicButton from '../../SVG/DeleteTopicButton'
  import EditTopicButton from '../../SVG/EditTopicButton'
  import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
  import axios from 'axios'
  import {mapGetters} from "vuex";

  const maxTeamRanksValue = 25;
  export default {
    name: "EditTeam",
    data() {
      return {
        description: '',
        file: null,
        baseInfo: '',
        rankFields: ['index', 'name', 'description', 'options'],
        editor: ClassicEditor,
        editorConfig: {},
        ranks: [],
        rankInput: {
          name: '',
          description: '',
        }
      }
    },
    components: {
      DeleteTopicButton,
      EditTopicButton
    },
    created() {
      if (!this.isTeamOwner) {
        this.$router.push({name: 'home'})
      }
      this.$store.dispatch('fetchUser')
      this.getTeamRanks()
      this.$store.dispatch('getTeamData', this.$store.state.authentication.user.teamID).then(
        () => {
          this.description = this.getTeam.description
          this.baseInfo = this.getTeam.baseInfo
        }
      )
    },
    methods: {
      addRank() {
        const data = {
          name: this.rankInput.name,
          description: this.rankInput.description,
          team: this.$store.state.authentication.user.teamID
        }
        axios.post('ranks/', data).then(
          (response) => {
            switch (response.status) {
              case 201:
                this.ranks.push(data)
            }
          }
        ).catch(
          (error) => {

          }
        )
        this.rankInput.name = ''
        this.rankInput.description = ''
      },
      removeRank() {

      },
      updateTeam() {
        const formData = new FormData();
        if (this.file) {
          formData.append('avatar', this.file);
        }
        formData.append('description', this.description);
        formData.append('base_info', this.baseInfo);
        axios.patch(`teams/${this.$route.params.teamID}/`, formData).then(
          (response) => {

            switch (response.status) {
              case 200:
                this.$store.dispatch('fetchUser');
                this.$router.push({
                  name: 'team',
                  params: {
                    teamID: this.$route.params.teamID
                  }
                });
                break;
              case 400:
                break;
              case 403:
                break;
            }
          }
        )
      },
      getTeamRanks() {
        const data = {
          teamID: this.$store.state.authentication.user.teamID
        }
        debugger
        axios.get('ranks/get-team-ranks/', {
          params: data
        }).then(
          (response) => {
            switch (response.status) {
              case 200:
                this.ranks = response.data
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
      }
    },
    computed: {
      ...mapGetters([
        'isTeamOwnerByTeamId',
        'getTeam',
        'getTeamName',
        'getTeamAvatar',
        'isTeamOwner',
      ]),
    }
  }
</script>

<style scoped>
  .danger-team-name-text {
    color: #FF4C33 !important;
  }
</style>
