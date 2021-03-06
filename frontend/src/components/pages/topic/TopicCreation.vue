<template>
  <div>
    <div class="row">
      <div class="col-lg-12">
        <div class="topic-creation-container">
          <h1>
            Topic Creation
          </h1>
          <div class="form-container">
            <b-form>
              <label for="input-topic-title">Topic Title:</label>
              <b-form-input
                id="input-topic-title"
                :state="validateState('title')"
                @blur="$v.title.$touch()"
                v-model="$v.title.$model"
                aria-describedby="input-live-help input-live-feedback"
                placeholder="Enter title of the topic"
                trim
              >
              </b-form-input>
              <small id="usernameHelp" class="form-text text-muted">{{titleSmallText}}</small>
              <label for="input-topic-description">Topic Description:</label>
              <b-form-input
                id="input-topic-description"
                :state="validateState('description')"
                @blur="$v.description.$touch()"
                v-model="$v.description.$model"
                aria-describedby="input-live-help input-live-feedback"
                placeholder="Enter title of the topic"
                trim
              >
              </b-form-input>

              <b-form-invalid-feedback id="input-live-feedback">
                Enter at least 3 letters
              </b-form-invalid-feedback>

              <label for="topic-body">Topic Body:</label>
              <ckeditor :editor="editor"
                        class="ck-content"
                        v-model="body"
                        :config="editorConfig">
              </ckeditor>
            </b-form>
            <div class="button-control">
              <vue-tags-input
                v-model="tag"
                :tags="tags"
                @tags-changed="newTags => tags = newTags"
              />
            </div>
            <div class="button-control">
              <b-button v-if="$v.$invalid"
                        disabled>
                Submit
              </b-button>
              <b-button v-else @click="createTopic" variant="success">
                Submit
              </b-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import {required, minLength} from 'vuelidate/lib/validators'
  import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

  export default {
    name: "TopicCreation",
    data() {
      return {
        title: "",
        description: "",
        body: "",
        editor: ClassicEditor,
        editorConfig: {},
        section: this.$route.params.section,
        tag: '',
        tags: [],
      }
    },
    validations: {

      title: {
        required,
        unique: function (val, vueInstance) {
          if (val === '') {
            return true;
          }
          const params = {
            searchBy: 'title',
            value: val,
            section: this.section.toUpperCase()
          };
          return axios.get(`topics/search/`, {params: params})
            .then(response => {
              return response.status === 204
            })
        },
        minLen: minLength(3)
      },
      description: {
        required,
        minLen: minLength(3)
      },
    },
    methods: {
      addTag() {
        this.tags.push(this.tag)
      },
      createTopic() {
        this.tags.forEach(
          tag => {
            tag["name"] = tag["text"]
          }
        )
        const data = {
          title: this.title,
          description: this.description,
          body: this.body,
          section: this.section.toUpperCase(),
          tags: this.tags
        };
        axios.post('topics/', data)
          .then((response) => {
            switch (response.status) {
              case 201:
                this.moveToCreatedTopic(response.data.topic_id);
                break;
              case 400:
                break;
              case 500:
                break;

            }
          })
      },
      moveToCreatedTopic(topicID) {
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
      }
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
