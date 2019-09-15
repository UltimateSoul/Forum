<template>
  <div>
    <div class="col-lg-10 col-md-6 col-sm-3">
      <form>
        <div class="form-group">
          <label for="exampleInputEmail1">Username</label>
          <input type="text"
                 class="form-control"
                 id="exampleInputEmail1"
                 aria-describedby="emailHelp"
                 v-model="username"
                 placeholder="Enter Username">
          <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
        </div>
        <div class="form-group">
          <label for="exampleInputPassword1">Password</label>
          <input type="password"
                 class="form-control"
                 id="exampleInputPassword1"
                 v-model="password"
                 placeholder="Password">
        </div>
        <button class="btn btn-primary" @click="loginClick">Login</button>
      </form>
    </div>
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
      loginClick() {
        let data = {
          username: this.username,
          password: this.password
        };
        Vue.axios.post('http://127.0.0.1:8000/login/api-token-auth/', data)
          .then((response) => {
            debugger;
            console.log(response);
            sessionStorage.setItem('auth_token', response.data.token)
          })
          .catch((response) => {
            debugger;
            console.log(response)
          })
      }
    }
  }
</script>

<style scoped>

</style>
