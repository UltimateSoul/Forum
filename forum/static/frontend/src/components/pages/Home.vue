<template>
  <div>

    <div class="row">
      <div class="col-lg-12 col-md-8 col-xs-5 m-md-4">
        <div class="card text-center">
          <div class="card-header">
            Hy {{ user.username }}
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
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    name: "Home",
    data() {
      return {
        show: false,
      }
    },
    created() {
      if (!this.isLogged) {
        this.$router.push({name: 'login'});
      }
    },
    computed: {
      ...mapGetters({
        isLogged: 'isLogged',
        user: 'getUserData'
      })
    }
  }
</script>

<style scoped>

  .auto-margin {
    margin: 30px auto 30px auto;
  }
</style>
