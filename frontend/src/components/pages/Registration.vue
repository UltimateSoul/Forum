<template>
  <div class="registration-container">
    <h1>Registration</h1>
    <div class="form-container">
      <form>
        <div class="form-group">
          <label for="usernameInput">Username</label>
          <input type="text"
                 class="form-control text-center"
                 id="usernameInput"
                 aria-describedby="emailHelp"
                 v-model="registrationForm.username"
                 placeholder="Enter Username">
          <small id="usernameHelp" class="form-text text-muted">Your site nickname.</small>
        </div>
        <div class="form-group">
          <label for="passwordInput">Password</label>
          <input type="password"
                 class="form-control text-center"
                 id="passwordInput"
                 v-model="registrationForm.password"
                 placeholder="Enter your password">
          <small id="passwordHelp" class="form-text text-muted">We'll never share your password with anyone else.
          </small>
        </div>
        <div class="form-group">
          <label for="confirmPasswordInput">Confirm Password</label>
          <input type="password"
                 class="form-control text-center"
                 id="confirmPasswordInput"
                 v-model="registrationForm.confirmPassword"
                 placeholder="Enter your confirm password">
          <small id="confirmPasswordHelp" class="form-text text-muted">We'll never share your password with anyone else.
          </small>
        </div>
        <div class="form-group">
          <label for="emailInput">Email</label>
          <input type="text"
                 class="form-control text-center"
                 id="emailInput"
                 aria-describedby="emailHelp"
                 v-model="registrationForm.email"
                 placeholder="awesome@gmail.com">
          <small id="emailHelp" class="form-text text-muted">You can customize special setting using this email.</small>
        </div>
        <div class="form-group">
          <label for="gameNickNameInput">Game Nickname</label>
          <input type="text"
                 class="form-control text-center"
                 id="gameNickNameInput"
                 aria-describedby="gameNickNameHelp"
                 v-model="registrationForm.gameNickName"
                 placeholder="Enter Game Nickname">
          <small id="gameNickNameHelp" class="form-text text-muted">Your in-game nickname.</small>
        </div>
        <div class="form-group">
          <label for="cityInput">City</label>
          <input type="text"
                 class="form-control text-center"
                 id="cityInput"
                 aria-describedby="cityHelp"
                 v-model="registrationForm.city"
                 placeholder="Enter your City">
          <small id="cityHelp" class="form-text text-muted">Your City.</small>
        </div>
        <div class="form-group">
          <label for="inputGender">Gender</label>
          <select id="inputGender" class="form-control text-center" v-model="registrationForm.gender">
            <option v-for="gender in genderChoices" :value="gender.value">{{ gender.text }}</option>
          </select>
        </div>
        <button class="btn btn-primary btn-lg" @click="prepareToSubmit">Submit</button>
      </form>
    </div>

  </div>
</template>

<script>

  export default {
    name: "Registration",
    data() {
      return {
        registrationForm: {
          username: '',
          password: '',
          confirmPassword: '',
          email: '',
          gameNickName: '',
          city: '',
          gender: '',
          avatar: ''
        },
        genderChoices: [
          {text: 'Male', value: 'male'},
          {text: 'Female', value: 'female'},
          {text: '-----', value: ''}
        ]
      }
    },
    methods: {
      prepareToSubmit() {
        // ToDo: add validation logic to the registration flow
        this.register()
      },
      register() {
        this.$store.dispatch('register', this.registrationForm)
      }
    },
    computed: {

    }
  }
</script>

<style scoped>
  .registration-container {
    margin-left: auto;
    margin-right: auto;
    padding: 30px;
    width: 80vw;
  }

  .form-container {
    margin-left: auto;
    margin-right: auto;
    width: 50vw;
  }
</style>
