<template>
  <div>
    <div class="row">
      <div class="col-lg-12">
        <h1>The Blood Way ORPG 2</h1>
        <div class="card text-center">
          <div class="card-header">
            Hy
          </div>
          <div class="card-body">
            <h5 class="card-title">Special title treatment</h5>
            <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
          <div class="card-footer text-muted">
            2 days ago
          </div>
        </div>
      </div>
    </div>

    <!--    <div class="row">-->
    <!--      <div class="col-lg-4">-->
    <!--        <div class="card" style="width: 18rem;" v-for="user in users">-->
    <!--          <img :src="user.imageURL" class="card-img-top" alt="...">-->
    <!--          <div class="card-body">-->
    <!--            <h5 class="card-title">{{ user.name }}</h5>-->
    <!--            <p class="card-text">Your level is {{ user.level }}</p>-->
    <!--            <a href="#" class="btn btn-primary">Your Hero: {{ user.hero }}</a>-->
    <!--          </div>-->
    <!--        </div>-->
    <!--      </div>-->
    <!--      <div class="col-lg-8">-->

    <!--      </div>-->
    <!--    </div>-->
  </div>
</template>

<script>
  import mapGetters from 'vuex'
  export default {
    name: "Home",
    data() {
      return {
        show: false,
        user: null
      }
    },
    created() {
      debugger;
      if (this.$store.getters.isLogged) {
        debugger;
        this.$store.dispatch('fetchUser', sessionStorage.getItem('auth_token'))
          .then((resp) => {
            debugger;
          })
      }
    },
    // computed: {
    //   ...mapGetters([
    //     'isLogged'
    //   ])
    // }
  }
</script>

<style scoped>

  .auto-margin {
    margin: 30px auto 30px auto;
  }
</style>
