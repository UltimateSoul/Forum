<template>
  <div>
    <div class="row">
      <div class="col-lg-12">
        <div class="topic-creation-container">
          <h1>
            Topic Editing
          </h1>
          <div class="form-container">
            <b-form>
              <label for="input-topic-description">Topic Description:</label>
              <b-form-input
                id="input-topic-description"
                :state="validateState('description')"
                @blur="$v.description.$touch()"
                v-model="$v.description.$model"
                aria-describedby="input-live-help input-live-feedback"
                placeholder="Enter description of the topic"
                trim
              >
              </b-form-input>

              <b-form-invalid-feedback id="input-live-feedback">
                Enter at least 3 letters
              </b-form-invalid-feedback>

              <label for="topic-body">Topic Body:</label>
              <b-form-textarea
                id="topic-body"
                :state="validateState('body')"
                @blur="$v.body.$touch()"
                v-model="$v.body.$model"
                placeholder="Enter something..."
                rows="3"
                max-rows="6"
              >
              </b-form-textarea>
              <b-form-invalid-feedback id="input-live-feedback">
                Enter at least 10 letters
              </b-form-invalid-feedback>
            </b-form>
            <div class="button-control">
              <b-button v-if="$v.$invalid"
                        disabled>
                Save
              </b-button>
              <b-button v-else @click="editTopic" variant="success">
                Save
              </b-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {required, minLength} from 'vuelidate/lib/validators'
  import {mapGetters} from 'vuex'
  import axios from 'axios';

  export default {
    name: "TopicEditing",
    data() {
      return {
        description: "",
        body: "",
        section: this.$route.params.section,
        topicID: this.$route.params.topicID,
        author: {
          avatar: '',
          gameNickName: '',
          username: '',
          pk: 0
        }
      }
    },
    created() {
      this.getData().then(
        () => {
          if (!this.isMainUser(this.author.pk)) {
            this.$router.push({
              name: 'topic',
              params: {
                section: this.section,
                topicID: this.topicID
              }
            })
          }
        }
      )
    },
    validations: {
      description: {
        required,
        minLen: minLength(3)
      },
      body: {
        required,
        minLen: minLength(10)
      }
    },
    methods: {
      getData() {
        return axios.get('topics/' + this.topicID + '/').then(
          (response) => {
            this.description = response.data.description;
            this.body = response.data.body;
            this.author.avatar = response.data.author.avatar;
            this.author.gameNickName = response.data.author.game_nickname;
            this.author.username = response.data.author.username;
            this.author.pk = response.data.author.pk;
            this.title = response.data.title;
          }
        )
      },
      editTopic() {
        const data = {
          description: this.description,
          body: this.body,
          id: this.$route.params.topicID,
          section: this.section.toUpperCase()
        };
        axios.patch('topics/', data)
          .then((response) => {
            switch (response.status) {
              case 200:
                this.moveToEditedTopic(response.data.topic_id);
                break;
              case 400:
                break;
              case 500:
                break;

            }
          })
      },
      moveToEditedTopic(topicID) {
        this.$router.push({
          name: 'topic',
          params: {
            section: this.section,
            topicID: topicID
          }
        })
      },
      validateState(name) {
        const {$dirty, $error} = this.$v[name];
        return $dirty ? !$error : null;
      },
    },
    computed: {
      titleSmallText() {
        if (this.title) {
          if (this.$v.title.unique) {
            if (this.$v.title.minLen)
              return 'Your title is unique';
            else {
              return 'Your title is too short'
            }
          } else {
            return 'Your title is not unique, please enter unique one'
          }
        } else {
          return "Your topic title."
        }
      },
      ...mapGetters(['isMainUser'])
    }
  }
</script>

<style scoped>
  .topic-creation-container {
    margin-left: auto;
    margin-right: auto;
    padding: 30px;
    width: 80vw;
  }
</style>
