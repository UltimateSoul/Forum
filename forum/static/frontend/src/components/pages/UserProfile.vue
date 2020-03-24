<template>
  <div>
    <b-container>
      <b-card
        :title="user.username"
        :img-src="user.avatar"
        img-alt="Image"
        img-top
        tag="article"
        class="mb-2"
        v-if="!isEditing"
      >
        <b-card-text>
          Game Nickname: {{user.game_nickname}}
        </b-card-text>
        <hr>
        <b-card-title>Additional information</b-card-title>
        <hr>
        <b-card-text v-show="user.birth_date">
          Birthday: {{user.birth_date}}
        </b-card-text>
        <b-card-text v-if="isMainUser">
          BloodConins: {{user.blood_coins}}
        </b-card-text>
        <b-card-text>
          Gender: {{user.gender}}
        </b-card-text>
        <b-card-text>
          Email: {{user.email}}
        </b-card-text>
      </b-card>
      <b-form v-else>
        <h5>Choose your avatar:</h5>
        <b-form-file
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choose an image file or drop it here..."
          drop-placeholder="Drop file here..."
        ></b-form-file>
        <hr>
        <h5>Choose your game nickname:</h5>
        <b-form-input
          id="input-2"
          v-model="editingUserData.game_nickname"
          required
          placeholder="Enter game nickname"
        ></b-form-input>
        <hr>
        <h5>Choose your birth date:</h5>
        <b-form-datepicker id="example-datepicker"
                           :max="maxDate"
                           v-model="editingUserData.birth_date"
                           class="mb-2"></b-form-datepicker>
        <hr>
        <h5>Choose your email:</h5>
        <b-form-input type="text"
                        class="form-control text-center"
                        id="emailInput"
                        aria-describedby="emailHelp"
                        :state="validateState('email')"
                        @blur="$v.editingUserData.email.$touch()"
                        v-model="$v.editingUserData.email.$model"
                        placeholder="awesome@gmail.com">

        </b-form-input>
        <hr>
        <h5>Write something about yourself:</h5>
        <b-form-textarea
          id="textarea"
          v-model="editingUserData.description"
          placeholder="Enter something..."
          rows="3"
          max-rows="6"
        ></b-form-textarea>
        <hr>
        <h5>Choose your gender:</h5>
        <select id="inputGender" class="form-control text-center" v-model="editingUserData.gender">
            <option v-for="gender in genderChoices" :value="gender.value">{{ gender.text }}</option>
        </select>
      </b-form>
      <div v-if="isMainUser" class="button-control">
        <b-button @click="isEditing = !isEditing" variant="outline-primary">
          {{editingText}}
        </b-button>
        <b-button v-if="isEditing && $v.$invalid" variant="outline-primary" disabled>
          Save
        </b-button>
        <b-button v-if="isEditing && !$v.$invalid" @click="saveUserProfile" variant="outline-primary">
          Save
        </b-button>

      </div>

    </b-container>
  </div>
</template>

<script>
  import axios from 'axios'
  import {required, email} from 'vuelidate/lib/validators'

  export default {
    name: "UserProfile",
    data() {
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const maxDate = new Date(today);
      maxDate.setFullYear(maxDate.getFullYear() -12);
      return {
        user: {},
        maxDate: maxDate,
        file: null,
        editingUserData: {},
        isEditing: false,
        genderChoices: [
          {text: 'Male', value: 'MALE'},
          {text: 'Female', value: 'FEMALE'},
          {text: '-----', value: 'OTHER'}
        ]
      }
    },
    validations: {
      editingUserData: {
        email: {
        required,
        email,
        unique: function (val, data) {
          if (val === '' || val === data.email) {
            return true;
          }
          return axios.get('users/?email=' + val)
            .then(res => {
              console.log('Unique: ', Object.keys(res.data).length === 0);
              return Object.keys(res.data).length === 0
            })
        }
      }
      }
    },
    created() {
      this.getUserProfile(this.$route.params.id)
    },
    watch: {
      '$route'(to, from) {
        this.getUserProfile(to.params.id)
      }
    },
    methods: {
      getUserProfile(id) {
        axios.get(`user/${id}`)
          .then((resp) => {
            this.user = resp.data;
            this.editingUserData = resp.data
          })
          .catch((resp) => {
            console.log('An error occurred')
          })
      },
      saveUserProfile() {
        this.editingUserData.avatar = this.file ? this.file : this.editingUserData.avatar;
        const formData = new FormData();
        formData.append('avatar', this.editingUserData.avatar);
        formData.append('game_nickname', this.editingUserData.game_nickname);
        formData.append('birth_date', this.editingUserData.birth_date);
        formData.append('email', this.editingUserData.email);
        formData.append('gender', this.editingUserData.gender);
        axios.patch(`user/${this.$route.params.id}`, formData)
        .then( (response) => {

        })
      },
      validateState(name) {
        const {$dirty, $error} = this.$v.editingUserData[name];
        return $dirty ? !$error : null;
      },
    },
    computed: {
      isMainUser() {
        const mainUser = this.$store.getters.getUserData;
        const mainUserID = mainUser.userID;
        return mainUserID === parseInt(this.$route.params.id)
      },
      editingText() {
        return this.isEditing ? 'Done' : "Edit"
      }
    }
  }
</script>

<style scoped>

</style>
