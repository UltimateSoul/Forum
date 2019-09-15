<template>
  <div>
    <input v-model="username" type="text" placeholder="username">
    <input v-model="password" type="password" placeholder="password">
    <button @click="login">Login</button>
  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import VueAxios from 'vue-axios'

  Vue.use(VueAxios, axios);

  export default {
    name: "Login",
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      login() {
        let data = {
          username: this.username,
          password: this.password
        };
        debugger;
        Vue.axios.post('http://127.0.0.1:8000/login/api-token-auth/', data)
          .then((response) => {
          console.log(response);
          debugger;
        })
          .catch((response) => {
            console.log(response);
            debugger;
          })
      }
    }
  }
</script>

<style scoped>

</style>
