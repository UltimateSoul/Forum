<template>
  <div class="registration-container">
    <h1>Registration</h1>
    <div class="form-container">
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text" id="basic-addon1">@</span>
        </div>
        <input type="text" class="form-control" placeholder="Username" aria-label="Username"
               aria-describedby="basic-addon1">
      </div>
    </div>

  </div>
</template>

<script>
  export default {
    name: "Registration"
  }
</script>

<style scoped>
  .registration-container {
    margin-left: auto;
    margin-right: auto;
    padding: 30px;
    width: 80vw;
    border-radius: 15px;
    background-color: #C1F4FC;
  }

  .form-container {
    margin-left: auto;
    margin-right: auto;
    width: 50vw;
  }
</style>
