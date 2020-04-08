<template>
  <div>
    <h1>Team Creation</h1>
    <div class="form-container">
      <b-form>
        <b-form-group label="Team Title" label-for="teamTitleInput">
          <b-form-input type="text"
                        class="form-control text-center"
                        id="teamTitleInput"
                        :maxlength="255"
                        aria-describedby="teamTitleHelp"
                        :state="validateState('name')"
                        @blur="$v.name.$touch()"
                        v-model="$v.name.$model"
                        placeholder="My Awesome Team"></b-form-input>
          <small id="teamTitleHelp" class="form-text text-muted"
                 :class="{'danger-team-name-text': !$v.name.unique}">
            {{ teamTitleSmallText }}
          </small>
        </b-form-group>
        <hr>
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
          <b-form-textarea
            id="teamBaseInfo"
            v-model="baseInfo"
            placeholder="Enter something..."
            rows="3"
            max-rows="6"
          ></b-form-textarea>
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
                  v-if="$v.$invalid"
                  disabled>Submit
          </button>
          <button type="button"
                  class="btn btn-primary btn-lg"
                  v-else
                  @click="createTeam"
          >Submit
          </button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {mapGetters} from "vuex";

  export default {
    name: "EditTeam",
    data() {
      return {
        description: '',
        file: null,
        baseInfo: '',
      }
    },
    created() {
      if (!this.isTeamOwner(this.$route.params.teamID)) {
        this.$router.push({
          name: 'home'
        })
      }
    },
    methods: {
      validateState(name) {
        const {$dirty, $error} = this.$v[name];
        return $dirty ? !$error : null;
      },
      createTeam() {
        const formData = new FormData();
        if (this.file) {
          formData.append('avatar', this.file);
        }
        formData.append('name', this.name);
        formData.append('description', this.description);
        formData.append('base_info', this.baseInfo);
        axios.post('teams/', formData).then(
          (response) => {
            switch (response.status) {
              case 201:
                this.$store.dispatch('fetchUser');
                this.$router.push({
                  name: 'team',
                  params: {
                    teamID: response.data.pk
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
      ]),
    }
  }
</script>

<style scoped>
  .danger-team-name-text {
    color: #FF4C33 !important;
  }
</style>
