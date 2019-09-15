<template>
    <div>
      <button @click="goToLogin">Go to Login Page</button>
    </div>
</template>

<script>
    export default {
        name: "Home",
        methods: {
          goToLogin() {
            this.$router.push({name: 'login'})
          }
        }
    }
</script>

<style scoped>

</style>
