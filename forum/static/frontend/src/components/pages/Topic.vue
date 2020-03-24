<template>
  <div>
    <h1>{{title}}</h1>
    <hr>
    <h5>{{description}}</h5>
    <div>
      <b-card no-body class="overflow-hidden">
        <b-row no-gutters>
          <b-col md="2">
            <b-card-img :src="'http://0.0.0.0:5000' + author.avatar" class="rounded-0"></b-card-img>
            <h5>{{author.username}}</h5>
            <h5>{{author.game_nickname}}</h5>
          </b-col>
          <b-col md="10">
            <b-card-body title="Horizontal Card">
              <b-card-text>
                {{body}}
              </b-card-text>
            </b-card-body>
          </b-col>
        </b-row>
      </b-card>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "Topic",
    data() {
      return {
        topicID: this.$route.params.topicID,
        title: "",
        description: "",
        body: "",
        author: null
      }
    },
    created() {
      this.getData()
    },
    methods: {
      getData() {
        axios.get('topics/' + this.topicID + '/').then(
          (response) => {
            this.title = response.data.title;
            this.description = response.data.description;
            this.body = response.data.body;
            this.author = response.data.author;
            this.title = response.data.title;
            this.title = response.data.title;
          }
        )
      }
    }
  }
</script>

<style scoped>

</style>
