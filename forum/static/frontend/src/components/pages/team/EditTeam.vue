<template>
  <div>
    <b-img height="250" width="250" :src="getTeamAvatar"></b-img>
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
  import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
  import axios from 'axios'
  import {mapGetters} from "vuex";

  export default {
    name: "EditTeam",
    data() {
      return {
        description: '',
        file: null,
        baseInfo: '',
        editor: ClassicEditor,
        editorConfig: {}
      }
    },
    created() {
      if (!this.isTeamOwner(this.$route.params.teamID)) {
        this.$router.push({
          name: 'home'
        })
      }
      this.$store.dispatch('getTeamData', this.$route.params.teamID).then(
        () => {
          this.description = this.getTeam.description
          this.baseInfo = this.getTeam.baseInfo
        }
      )
    },
    methods: {
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
      }
    },
    computed: {
      ...mapGetters([
        'isTeamOwner',
        'getTeam',
        'getTeamName',
        'getTeamAvatar',
      ]),
    }
  }
</script>

<style scoped>
  .danger-team-name-text {
    color: #FF4C33 !important;
  }
</style>
