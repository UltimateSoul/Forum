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
            <h5>{{author.gameNickName}}</h5>
          </b-col>
          <b-col md="10">
            <b-card-body>
              <b-card-text>
                {{body}}
              </b-card-text>
            </b-card-body>
          </b-col>
        </b-row>
      </b-card>
      <div class="button-control" v-if="isMainUser(author.pk)">
        <b-button @click="editTopic">Edit</b-button>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import {mapGetters} from 'vuex';

  export default {
    name: "Topic",
    data() {
      return {
        topicID: this.$route.params.topicID,
        title: "",
        description: "",
        body: "",
        author: {
          avatar: '',
          gameNickName: '',
          username: '',
          pk: 0
        }
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
            this.author.avatar = response.data.author.avatar;
            this.author.gameNickName = response.data.author.game_nickname;
            this.author.username = response.data.author.username;
            this.author.pk = response.data.author.pk;
            this.title = response.data.title;
          }
        )
      },
      editTopic() {
        this.$router.push({
          name: 'topic-editing',
          params: {
            section: this.$route.params.section,
            topicID: this.topicID
          }
        })
      }
    },
    computed: {
      ...mapGetters([
        'isMainUser'
      ])
    }
  }
</script>

<style scoped>

</style>
