<template>
  <div>
    <div class="row">
      <div class="col-lg-12">
        <h1>
          Topic Creation
        </h1>
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
    name: "TopicCreation",

    methods: {
      createTopic() {
        Vue.axios.post('')
      }
    }
  }
</script>

<style scoped>

</style>
