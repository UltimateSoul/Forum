<template>
  <div id="app">
    <sidebar></sidebar>
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
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
