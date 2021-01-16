<template>
  <div>
    <div class="alert alert-danger"
         role="alert" v-if="dangerShow">
      An error occurred during the authentication process. Try again!
    </div>
    <div class="alert alert-success"
         role="alert" v-if="isLogged">
      You've successfully logged in!
    </div>
  </div>
</template>

<script>
  // ToDo: finish component
  export default {
    name: "alert",
    data() {
      return {
        successText: '',
        warningText: '',
        dangerText: '',
      }
    }
  }
</script>

<style scoped>

</style>
