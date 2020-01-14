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
                 v-model="username"
                 placeholder="Enter Username">
          <small id="usernameHelp" class="form-text text-muted">Your site nickname.</small>
        </div>
        <div class="form-group">
          <label for="passwordInput">Password</label>
          <input type="password"
                 class="form-control text-center"
                 id="passwordInput"
                 v-model="password"
                 placeholder="Enter your password">
          <small id="passwordHelp" class="form-text text-muted">We'll never share your password with anyone else.
          </small>
        </div>
        <div class="form-group">
          <label for="confirmPasswordInput">Confirm Password</label>
          <input type="password"
                 class="form-control text-center"
                 id="confirmPasswordInput"
                 @blur="$v.confirmPassword.$touch()"
                 v-model="confirmPassword"
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
                 @blur="$v.email.$touch()"
                 v-model="email"
                 placeholder="awesome@gmail.com">
          <small id="emailHelp" class="form-text text-muted"
                 :class="{'danger-email-text': !$v.email.unique}">{{ emailSmallText }}</small>
        </div>
        <div class="form-group">
          <label for="gameNickNameInput">Game Nickname</label>
          <input type="text"
                 class="form-control text-center"
                 id="gameNickNameInput"
                 aria-describedby="gameNickNameHelp"
                 v-model="gameNickName"
                 placeholder="Enter Game Nickname">
          <small id="gameNickNameHelp" class="form-text text-muted">Your in-game nickname.</small>
        </div>
        <div class="form-group">
          <label for="inputGender">Gender</label>
          <select id="inputGender" class="form-control text-center" v-model="gender">
            <option v-for="gender in genderChoices" :value="gender.value">{{ gender.text }}</option>
          </select>
        </div>

        <button type="button"
                class="btn btn-primary btn-lg"
                v-if="$v.$invalid"
                disabled>Submit
        </button>
        <button type="button"
                class="btn btn-primary btn-lg"
                v-else
                @click="prepareToSubmit"
        >Submit
        </button>
      </form>
    </div>

  </div>
</template>

<script>
  import { required, email, minLength, sameAs } from 'vuelidate/lib/validators'
  import axios from 'axios';

  export default {
    name: "Registration",
    data() {
      return {
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
        gameNickName: '',
        gender: '',
        avatar: '',
        genderChoices: [
          {text: 'Male', value: 'MALE'},
          {text: 'Female', value: 'FEMALE'},
          {text: '-----', value: 'OTHER'}
        ]
      }
    },
    validations: {
      email: {
        required,
        email,
        unique: val => {
          if (val === '') {
            return true;
          }
          return axios.get('users/?email=' + val)
            .then(res => {
              console.log('Unique: ', Object.keys(res.data).length === 0);
              return Object.keys(res.data).length === 0
            })
        }
      },
      password: {
        required,
        minLen: minLength(6)
      },
      confirmPassword: {
        required,
        sameAs: sameAs('password')
      }
    },
    methods: {
      prepareToSubmit() {
        // ToDo: add validation logic to the registration flow
        this.register()
      },
      register() {
        let data = {
          username: this.username,
          password: this.password,
          email: this.email,
          gameNickName: this.gameNickName,
          gender: this.gender,
          avatar: this.avatar,
        };
        this.$store.dispatch('register', data)
      }
    },
    computed: {
      emailSmallText() {
        if (this.email) {
          if (this.$v.email.unique) {
          return 'Your email is unique'
        } else {
          return 'Your email is not unique, please enter unique one'
        }
        }
      }
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
  .danger-email-text {
    color: #FF4C33 !important;
  }
</style>
