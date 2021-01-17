<template>
  <div>
    <v-autocomplete
      v-model="elasticSearch.select"
      :items="elasticSearch.suggestions"
      :search-input.sync="elasticSearch.search"
      class="mx-4"
      flat
      hide-no-data
      hide-details
      label="Search topics in that section by title"
      solo-inverted
    ></v-autocomplete>

    <div style="margin: 40px">
      <template slot="suggestion" slot-scope="{ data }">
        {{ data.elasticSearch.suggestions }}
      </template>
    </div>
    <modal name="searchedTopic"
           v-if="Boolean(searchedTopic)"
           :draggable="true"
           :aria-expanded="true"
           height="30%"
           width="50%">
      <div>
        <div @click="moveToTopic(searchedTopic.id)">
          <b-card no-body class="overflow-hidden"
                  @click="moveToTopic(searchedTopic.id)">
            <b-row no-gutters>
              <b-col md="6">
                <b-card-img :src="searchedTopic.author.avatar" alt="Image" class="rounded-0"></b-card-img>
              </b-col>
              <b-col md="6">
                <b-card-body :title="searchedTopic.title">
                  <b-card-text>
                    {{ searchedTopic.description }}
                  </b-card-text>
                  <b-button @click="moveToTopic(topic.id)" class="primary">
                    go to that topic
                  </b-button>
                </b-card-body>
              </b-col>
            </b-row>
          </b-card>
        </div>
      </div>
    </modal>
    <div class="row">
      <div class="col-lg-8">
        <h1>Conversation</h1>
      </div>
      <div class="col-lg-4">
        <button class="btn btn-dark" v-if="$store.getters.isLogged" @click="createTopic">
          Create Topic
        </button>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12 col-md-10 col-xs-5">
        <table class="table" v-if="!loading">
          <thead>
          <tr>
            <th scope="col">Topic</th>
            <th scope="col">Responses</th>
            <th scope="col">Author</th>
            <th scope="col">Edited Date</th>
          </tr>
          </thead>
          <tbody name="slide" is="transition-group">
          <tr v-for="(topic, index) in topics" :key="index"
              @click="moveToTopic(topic.id)" class="clickable">

            <th>
              {{ topic.title }}
            </th>
            <td>{{ topic.posts_quantity }}</td>
            <td>{{ topic.author.username }}</td>
            <td>{{ topic.edited_at | getDateFormat }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios);
  export default {
    name: "Conversation",
    data() {
      return {
        loading: false,
        topics: [],
        testQuantity: 2,
        section: this.$route.params.section,
        elasticSearch: {
          suggestions: [],
          select: null,
          search: null
        },
        searchedTopic: {
          title: '',
          description: '',
          author: {
            avatar: ''
          }
        }
      }
    },
    created() {
      this.loading = true;
      this.getData()
    },
    watch: {
      'elasticSearch.search'(val) {
        val && val !== this.select && this.getSuggestions(val)
      },
      'elasticSearch.select'(val) {
        let id;
        this.elasticSearch.suggestions.forEach((suggestion)=> {
          if (suggestion.text === val) {
            id = suggestion.id
          }
        })
        this.searchTopicByID(id)
      }
    },
    methods: {
      getData() {
        axios.get(`topics/by-section/`, {params: {section: this.section.toUpperCase()}}).then((resp) => {
          this.topics = resp.data;
        })
          .finally(() => {
            this.loading = false;
          })
      },
      createTopic() {
        this.$router.push({name: 'topic-creation'})
      },
      moveToTopic(topicID) {
        this.$router.push({
          name: 'topic',
          params: {
            section: this.section,
            topicID: topicID
          }
        })
      },
      getSuggestions(v) {
        axios.get('core/search-topics/', {
          params: {
            query: this.elasticSearch.search,
            section: this.$route.params.section
          }
        }).then(
          (response) => {
            switch (response.status) {
              case 200:
                this.elasticSearch.suggestions = response.data;
                break
              default:
            }
          }
        )
      },
      showSearchedTopic() {
        this.$modal.show('searchedTopic')
      },
      hideSearchedTopic() {
        this.$modal.hide('searchedTopic')
      },
      searchTopicByID(topicID) {
        console.log(`I'm searching topic by title: "${this.elasticSearch.search}"`)
        axios.get(`topics/${topicID}/`).then(
          response => {
            switch (response.status) {
              case 200:
                this.searchedTopic = response.data;
                this.showSearchedTopic()
            }
          }
        )
      }
    },
    filters: {
      getDateFormat(value) {
        let dateObj = new Date(value);
        let date = dateObj.toLocaleDateString();
        let time = dateObj.toLocaleTimeString();
        return `${date}  ${time}`
      }
    }
  }
</script>

<style scoped>
  .clickable {
    cursor: pointer;
  }
</style>
