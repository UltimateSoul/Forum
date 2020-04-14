<template>
  <div>
    <modal name="confirm-email" :clickToClose="false">
      <div>
        <v-alert dense text type="success">
        You've been successfully <strong>registered</strong>!
      </v-alert>
        <h1>One more step!</h1>
        <p class="text-justify">
          We've sent confirmation link to your email. Please, consider activating your account to start using our awesome forum!
        </p>
        <b-button variant="success" @click="hideConfirmEmail">
          Ok
        </b-button>
      </div>
    </modal>
    <h1>Registration</h1>
    <div class="form-container">
      <b-form>
        <b-form-group label="Username" label-for="usernameInput">
          <b-form-input type="text"
                        class="form-control text-center"
                        id="usernameInput"
                        aria-describedby="emailHelp"
                        v-model="$v.username.$model"
                        :state="validateState('username')"
                        placeholder="Enter Username">

          </b-form-input>
          <small id="usernameHelp" class="form-text text-muted">{{usernameSmallText}}</small>
        </b-form-group>
        <b-form-group label="Password" label-for="passwordInput">
          <b-form-input type="password"
                        class="form-control text-center"
                        id="passwordInput"
                        v-model="$v.password.$model"
                        :state="validateState('password')"
                        placeholder="Enter your password"></b-form-input>
          <small id="passwordHelp" class="form-text text-muted">
            We'll never share your password with anyone else.
          </small>
        </b-form-group>
        <b-form-group label="Confirm Password" label-for="confirmPasswordInput">
          <b-form-input type="password"
                        class="form-control text-center"
                        id="confirmPasswordInput"
                        :state="validateState('confirmPassword')"
                        @blur="$v.confirmPassword.$touch()"
                        v-model="$v.confirmPassword.$model"
                        placeholder="Enter your confirm password"></b-form-input>
          <small id="confirmPasswordHelp" class="form-text text-muted">
            We'll never share your password with anyone else.
          </small>
        </b-form-group>
        <b-form-group label="Email" label-for="emailInput">
          <b-form-input type="text"
                        class="form-control text-center"
                        id="emailInput"
                        aria-describedby="emailHelp"
                        :state="validateState('email')"
                        @blur="$v.email.$touch()"
                        v-model="$v.email.$model"
                        placeholder="awesome@gmail.com"></b-form-input>
          <small id="emailHelp" class="form-text text-muted"
                 :class="{'danger-email-text': !$v.email.unique}">
            {{ emailSmallText }}
          </small>
        </b-form-group>
        <b-form-group label="Game Nickname" label-for="usernameInput">
          <b-form-input type="text"
                        class="form-control text-center"
                        id="gamenicknameInput"
                        aria-describedby="GameNickNameHelp"
                        v-model="gameNickName"
                        placeholder="Enter Game nickname">

          </b-form-input>
          <small id="GameNickNameHelp" class="form-text text-muted">Your in-game nickname.</small>
        </b-form-group>
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
                @click="register"
        >Submit
        </button>
      </b-form>
    </div>
  </div>
</template>

<script>
  import {required, email, minLength, sameAs} from 'vuelidate/lib/validators'
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
        avatar: null,
        genderChoices: [
          {text: 'Male', value: 'MALE'},
          {text: 'Female', value: 'FEMALE'},
          {text: '-----', value: 'OTHER'}
        ],
        showConfirmEmailModal: false,
      }
    },
    validations: {
      username: {
        required,
        minLen: minLength(2),
        unique: val => {
          if (val === '') {
            return true;
          }
          return axios.get('users/search/?username=' + val)
            .then(res => {
              console.log('Unique: ', Object.keys(res.data).length === 0);
              return Object.keys(res.data).length === 0
            })
        }
      },
      email: {
        required,
        email,
        unique: val => {
          if (val === '') {
            return true;
          }
          return axios.get('users/search/?email=' + val)
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
      showconfirmEmail() {
        this.$modal.show('confirmEmail')
      },
      hideConfirmEmail() {
        this.$modal.hide('confirmEmail')
        this.$router.push('home')
      },
      register() {
        let data = {
          username: this.username,
          password: this.password,
          email: this.email,
          game_nickname: this.gameNickName,
          gender: this.gender ? this.gender : 'OTHER',
          avatar: this.avatar,
        };
        this.$store.dispatch('register', data).then(
          () => {
            if (this.$store.getters.isLogged) {
              this.showconfirmEmail()
            }
          }
        )
      },
      validateState(name) {
        const {$dirty, $error} = this.$v[name];
        return $dirty ? !$error : null;
      },
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
      },
      usernameSmallText() {
        if (this.username) {
          if (this.$v.username.unique) {
            if (this.$v.username.minLen)
              return 'Your username is unique';
            else {
              return 'Your username is too short'
            }
          } else {
            return 'Your username is not unique, please enter unique one'
          }
        } else {
          return "Your site nickname."
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
