<template>
  <div>
    <!--  <Menu/>-->
    <!--    <main id="page-wrap">-->
    <Reveal>
      <router-link to="/">
        <span> Home </span>
      </router-link>
      <a @click="loginClick">
        <span> {{ logText }} </span>
      </a>
      <router-link to="/shop" v-if="isLogged">
        <span> Shop </span>
      </router-link>
      <router-link to="/get-started">
        <span> Get&nbspStarted </span>
      </router-link>
      <router-link to="/sections" v-if="isLogged">
        <span> Sections </span>
      </router-link>
      <router-link to="/teams" v-if="isLogged">
        <span> Teams </span>
      </router-link>
      <a @click="profileClick" v-if="isLogged">
        <span> Profile </span>
      </a>
    </Reveal>
    <!--    </main>-->
  </div>
</template>

<script>
  import { mapMutations, mapGetters } from 'vuex';
  import { Reveal } from 'vue-burger-menu'
  // import the CSS transitions you wish to use, in this case we are using `Slide`

  export default {
    name: "Sidebar",
    components: {
      Reveal // Register your component
    },
    methods: {
      loginClick() {
        if (this.isLogged) {
          this.$router.push({name: 'login'});
          this.$store.commit('logout');

        } else {
          this.$router.push({name: 'login'})
        }
      },
      profileClick() {
        const userData = this.$store.getters.getUserData;
        this.$router.push({name: 'user-profile',
                           params: {
                              id: userData.userID
                           }})
      }
    },
    computed: {
      ...mapGetters([
        'isLogged',
      ]),
      ...mapMutations([
        'logout',
      ]),
      logText() {
        return this.isLogged ? 'Logout' : 'Login'
      }
    }
  }

</script>

<style scoped>
  a {
    text-decoration: none;
  }

  .bm-burger-button {
    position: fixed;
    width: 36px;
    height: 30px;
    left: 36px;
    top: 36px;
    cursor: pointer;
  }

  .bm-burger-bars {
    background-color: #2e303c;
  }

  .line-style {
    position: absolute;
    height: 20%;
    left: 0;
    right: 0;
  }

  .cross-style {
    position: absolute;
    top: 12px;
    right: 2px;
    cursor: pointer;
  }

  .bm-cross {
    background: #bdc3c7;
  }

  .bm-cross-button {
    height: 24px;
    width: 24px;
  }

  .bm-menu {
    height: 100%; /* 100% Full-height */
    width: 0; /* 0 width - change this with JavaScript */
    position: fixed; /* Stay in place */
    z-index: 1000; /* Stay on top */
    top: 0;
    left: 0;
    background-color: #2e303c; /* Black*/
    overflow-x: hidden; /* Disable horizontal scroll */
    padding-top: 60px; /* Place content 60px from the top */
    transition: 0.5s; /*0.5 second transition effect to slide in the sidenav*/
  }

  .bm-overlay {
    background: rgba(0, 0, 0, 0.3);
  }

  .bm-item-list {
    color: #da6868;
    margin-left: 10%;
    font-size: 24px;
  }

  .bm-item-list > * {
    cursor: pointer;
    display: flex;
    text-decoration: none;
    padding: 0.7em;
  }

  .bm-item-list > * > span {
    margin-left: 10px;
    font-weight: 700;
    color: #ffffff;
  }
</style>
