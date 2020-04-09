<template>
  <div>
    <vue-bootstrap-typeahead
      v-model="elasticSearch.query"
      @input="getSuggestions"
      :data="elasticSearch.suggestions"
    />
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
          query: ''
        }
      }
    },
    created() {
      this.loading = true;
      this.getData()
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
      getSuggestions() {
        axios.get('http://0.0.0.0:5000/core/search-topics/', {
          params: {
            query: this.elasticSearch.query
          }
        }).then(
          (response) => {
            switch (response.status) {
              case 200:
                this.elasticSearch.suggestions = response.data.suggestions;
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
