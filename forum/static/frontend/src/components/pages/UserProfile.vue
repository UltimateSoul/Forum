<template>
  <div>
    <div>
      <b-card
        :title="user.username"
        :img-src="user.avatar"
        img-alt="Image"
        img-top
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          Game Nickname: {{user.game_nickname}}
        </b-card-text>
        <hr>
      <b-card-title>Additional information</b-card-title>
      <hr>
        <b-card-text v-show="user.birth_date">
          Birthday: {{user.birth_date}}
        </b-card-text>
        <b-card-text v-if="isMainUser">
          BloodConins: {{user.blood_coins}}
        </b-card-text>
        <b-card-text>
          Gender: {{user.gender}}
        </b-card-text>
        <b-card-text>
          Email: {{user.email}}
        </b-card-text>
      </b-card>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios);
  export default {
    name: "UserProfile",
    data() {
      return {
        user: {},
        isEditing: false

      }
    },
    created() {
      this.getUserProfile(this.$route.params.id)
    },
    watch: {
      '$route'(to, from) {
        this.getUserProfile(to.params.id)
      }
    },
    methods: {
      getUserProfile(id) {
        Vue.axios.get(`user/${id}`)
          .then((resp) => {
            this.user = resp.data
          })
          .catch((resp) => {
            console.log('An error occurred')
          })
      }
    },
    computed: {
      isMainUser() {
        const mainUser = this.$store.getters.getUserData;
        const mainUserID = mainUser.userID;
        return mainUserID === parseInt(this.$route.params.id)
      }
    }
  }
</script>

<style scoped>

</style>
