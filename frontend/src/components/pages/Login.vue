<template>
  <div class="row">
    <div class="col-lg-12 col-md-6 col-sm-3 justify-content-center">
      <div class="alert alert-danger"
           role="alert" v-if="dangerShow">
        An error occurred during the authentication process. Try again!
      </div>
      <div class="alert alert-success"
           role="alert" v-if="isLogged">
        You've successfully logged in!
      </div>
      <form v-if="!isLogged">
        <div class="login-container">
          <div class="form-group">
            <label for="exampleInputEmail1">Username</label>
            <input type="text"
                   class="form-control"
                   id="exampleInputEmail1"
                   aria-describedby="emailHelp"
                   v-model="username"
                   placeholder="Enter Username">
            <small id="emailHelp" class="form-text text-muted">We'll never share your password with anyone else.</small>
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
          <router-link :to="{name: 'registration'}"><button class="btn btn-primary">
            Register
          </button></router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import VueAxios from 'vue-axios'
  import {mapMutations, mapGetters} from 'vuex';

  Vue.use(VueAxios, axios);

  export default {
    name: "Login",
    data() {
      return {
        username: '',
        password: '',
        dangerShow: false,
      }
    },
    methods: {
      ...mapMutations([
        'loginAndLogout'
      ]),
      loginClick() {
        let data = {
          username: this.username,
          password: this.password
        };
        this.$store.dispatch('login', data)
          .catch((response) => {
            this.dangerShow = true;
          })
      },
      homePageClick() {
        this.$router.push({name: 'home'});
      }
    },
    watch: {
      isLogged(value) {
        if (value) {
          this.$router.push({name: 'home'});
        }
      }
    },
    computed: {
      ...mapGetters([
        'isLogged'
      ])
    }
  }
</script>

<style scoped>
  .login-container {
    margin-left: auto;
    margin-right: auto;
    width: 60vw;
  }
</style>
