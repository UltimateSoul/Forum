<template>
  <div id="app">
    <sidebar></sidebar>
    <main id="page-wrap">
      <div class="container-fluid">
          <div class="page-container">
            <transition name="slide" mode="out-in">
            <router-view/>
            </transition>
          </div>
      </div>
    </main>
  </div>
</template>

<script>
  import Sidebar from './components/Sidebar'
  // import Header from './components/Header'
  // import Footer from './components/Footer'

  export default {
    name: 'App',
    created() {
      let token = sessionStorage.getItem('auth_token');
      if (Boolean(token)) {
        this.$store.commit('setAuthToken');
        this.$store.dispatch('fetchUser')
      } else {
        this.$router.push(
          {name: 'login'}
        )
      }
    },
    components: {
      sidebar: Sidebar
      // headerComponent: Header,
      // footerComponent: Footer
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Comfortaa:400,700&display=swap');

  #app {
    font-family: 'Comfortaa', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  .clicable {
    cursor: pointer;
  }

  .page-container {
    margin-left: auto;
    margin-right: auto;
    padding: 30px;
    width: 80vw;
  }

  .button-control {
    margin: 15px;
  }

  .slide-enter {
    opacity: 0;
  }

  .slide-enter-active {
    animation: slide-in 1s ease-out forwards;
    transition: opacity 1s;
  }

  .slide-leave {

  }

  .slide-leave-active {
    animation: slide-out 1s ease-out forwards;
    transition: opacity 1s;
    opacity: 0;
  }

  @keyframes slide-in {
    from {
      transform: translateY(20px);
    }
    to {
      transform: translateY(0);
    }
  }

  @keyframes slide-out {
    from {
      transform: translateY(0);
    }
    to {
      transform: translateY(20px);
    }
  }
</style>
