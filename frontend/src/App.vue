<template>
  <div id="app">
    <sidebar></sidebar>
<!--    <main id="page-wrap">-->
<!--      <router-view/>-->
<!--    </main>-->
    <div class="container">
      <router-view/>
    </div>
  </div>
</template>

<script>

  import Sidebar from './components/Sidebar'

  export default {
    name: 'App',
    components: {
      sidebar: Sidebar
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
</style>
