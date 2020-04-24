<template>
  <div>
      <div class="center-card">
        <b-card no-body class="overflow-hidden special-card" style="max-width: 540px;">
          <b-row no-gutters>
            <b-col md="6">
              <b-card-img :src="user.avatar ? user.avatar : 'http://0.0.0.0:5000/static/images/default.jpg'" alt="Image" class="rounded-0"></b-card-img>
            </b-col>
            <b-col md="6">
              <b-card-body :title="user.username">
                You are with us for {{ getDaysHere() }} days.
              </b-card-body>
            </b-col>
          </b-row>
        </b-card>
      </div>
      <b-row class="button-control">
        <b-col>
          <router-link to="/get-started">
            <b-button variant="dark">Get Started</b-button>
          </router-link>
        </b-col>
        <b-col>
          <b-button variant="dark" @click="profileClick">Profile</b-button>
        </b-col>
      </b-row>
      <div v-if="popularTopics.length">
        <h1>
          The most popular topics:
        </h1>
        <b-table @row-clicked="clickTopic"
                 striped hover
                 class="clicable"
                 :items="popularTopics"
                 :fields="fields">
          <template v-slot:cell(avatar)="data">
            <img :src="data.item.author.avatar ? data.item.author.avatar : 'http://0.0.0.0:5000/static/images/default.jpg'" height="100" width="100">
          </template>
          <template v-slot:cell(created_at)="data">
            {{ data.item.created_at | getDateFormat }}
          </template>
        </b-table>
      </div>
    </div>
</template>

<script>
  import axios from 'axios'
  import {mapGetters} from 'vuex'

  export default {
    name: "Home",
    data() {
      return {
        fields: ['avatar', 'title', 'description', 'posts_quantity'],
        show: false,
        popularTopics: [],
        loading: false,
      }
    },
    created() {
      if (!this.isLogged) {
        this.$router.push({name: 'login'});
      }
      this.getPopularTopics()
    },
    methods: {
      getDaysHere() {
        const oneDay = 24 * 60 * 60 * 1000;
        const now = Date.now()
        return Math.round(Math.abs((now - this.user.dateJoined) / oneDay));
      },
      getPopularTopics() {
        this.loading = true
        axios.get('http://0.0.0.0:5000/core/get-popular-topics/').then(
          (response) => {
            switch (response.status) {
              case 200:
                this.popularTopics = response.data;
                this.loading = false
                break
              default:
                this.loading = false
                break
            }
          }
        )
      },
      profileClick() {
        this.$router.push({
          name: 'user-profile',
          params: {
            id: this.user.userID
          }
        })
      },
      clickTopic(rowData) {
        this.$router.push({
          name: 'topic',
          params: {
            section: rowData.section,
            topicID: rowData.id
          }
        })
      }
    },
    computed: {
      ...mapGetters({
        isLogged: 'isLogged',
        user: 'getUserData',
      })
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

  .auto-margin {
    margin: 30px auto 30px auto;
  }

  .center-card {
    text-align: -webkit-center;
  }
</style>
