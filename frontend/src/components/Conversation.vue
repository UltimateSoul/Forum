<template>
  <div>
    <div class="row">
      <div class="col-lg-8">
        <h1>Conversation</h1>
      </div>
      <div class="col-lg-4">
        <button class="btn btn-dark" @click="createTopic">
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
            <th scope="col">Created Date</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="topic in topics">
            <th scope="row">{{ topic.title }}</th>
            <td>{{ topic.posts_quantity }}</td>
            <td>{{ topic.author.username }}</td>
            <td>{{ topic.created_date | getDateFormat }}</td>
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
        topics: []
      }
    },
    created() {
      this.loading = true;
      this.getData()
    },
    methods: {
      getData() {
        let data = {section: 'IDEAS'};
        Vue.axios.get('http://127.0.0.1:8000/api/conversation/topics/', {params: data})
          .then((resp) => {
            this.topics = resp.data;
          })
          .finally(() => {
            this.loading = false;
          })
      },
      createTopic() {
        this.$router.push('topic-creation')
      }
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
