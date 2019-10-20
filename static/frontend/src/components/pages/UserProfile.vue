<template>
  <div>
    <div class="card text-center">
      <div class="card-header">
        {{ }}
      </div>
      <div class="card-body">
        <h5 class="card-title">{{ username }}</h5>
        <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
        <p class="card-text">Bloodcoins: {{ blood_coins }}</p>
      </div>
      <div class="card-footer text-muted">
        2 days ago
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
    name: "UserProfile",
    data() {
      return {
        username: '',
        blood_coins: '',

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
        Vue.axios.get(`http://127.0.0.1:8000/api/conversation/user/${id}`)
          .then((resp) => {
            let data = resp.data[0];
            this.username = data.first_name + ' ' + data.last_name;
            this.blood_coins = data.blood_coins;
            console.log(resp.data)
          })
          .catch((resp) => {
            console.log('An error occurred')
          })
      }
    }
  }
</script>

<style scoped>

</style>
