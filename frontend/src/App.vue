<template>
  <v-app>
    <div id="app">
      <sidebar></sidebar>
      <main id="page-wrap">
        <div class="container-fluid">
          <div class="page-container">
            <div v-for="notification in notifications"
                 v-if="notifications.length"
                 class="clickable"
                 @click="deleteNotification(notification.id)">
              <v-alert
                :type="getNotificationType(notification.notification_type)"
                :key="notification.id">
                {{ notification.message }}
              </v-alert>
            </div>
            <transition
              name="fade"
              mode="out-in"
              @beforeLeave="beforeLeave"
              @enter="enter"
              @afterEnter="afterEnter">
              <router-view/>
            </transition>
          </div>
        </div>
      </main>
    </div>
  </v-app>
</template>

<script>
  import axios from 'axios'
  import Sidebar from './components/Sidebar'
  // // import Header from './components/Header'
  // // import Footer from './components/Footer'

  export default {
    name: 'App',
    data() {
      return {
        notifications: [],
        prevHeight: 0,
      }
    },
    watch: {
      $route (to, from){
        this.$store.dispatch('fetchUser')
        this.getNotifications();
    }
    },
    created() {
      let token = localStorage.getItem('auth_token');
      if (Boolean(token)) {
        this.$store.commit('setAuthToken');
        this.$store.dispatch('fetchUser')
      } else {
        this.$router.push(
          {name: 'login'}
        )
      }
      if (this.$store.getters.isLogged) {
        setInterval(this.getNotifications, 45000);
      }
    },
    methods: {
      beforeLeave(element) {
        this.prevHeight = getComputedStyle(element).height;
      },
      enter(element) {
        const {height} = getComputedStyle(element);

        element.style.height = this.prevHeight;

        setTimeout(() => {
          element.style.height = height;
        });
      },
      afterEnter(element) {
        element.style.height = 'auto';
      },
      getNotifications() {
        axios.get('backend/core/notifications-list/').then(
          (response) => {
            switch (response.status) {
              case 200:
                this.notifications = response.data;
                break;
            }
          }
        )
      },
      deleteNotification(notificationID) {
        axios.delete(`backend/core/delete-notification/${notificationID}/`).then(
          (response) => {
            switch (response.status) {
              case 204:
                this.getNotifications()
            }
          }
        )
      },
      getNotificationType(notificationTypeNumber) {
        switch (notificationTypeNumber) {
          case 1:
            return 'success';
          case 2:
            return 'info';
          case 3:
            return 'warning';
          case 4:
            return 'error';
        }
      }
    },
    components: {
      sidebar: Sidebar,
      // VueBootstrapTypeahead,
      // headerComponent: Header,
      // footerComponent: Footer
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Comfortaa:400,700&display=swap');

  #app {
    font-family: 'Comfortaa', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  .tag-container {
    color: white;
    background-color: #343a40;
    margin: 5px;
    padding: 5px;
    border: solid 1px;
    border-radius: 10px;
    font-size: 20px;
  }

  .clickable {
    cursor: pointer;
  }

  .fade-enter-active,
  .fade-leave-active {
    transition-duration: 0.3s;
    transition-property: height, opacity;
    transition-timing-function: ease;
    overflow: hidden;
  }

  .fade-enter,
  .fade-leave-active {
    opacity: 0
  }

  .special-card {
    background-color: rgba(245, 245, 245, 1);
    opacity: .95;
  }

  .spinner-style {
    width: 5rem;
    height: 5rem;
  }

  .page-container {
    margin-left: auto;
    margin-right: auto;
    padding: 30px;
    width: 90vw;
  }

  .button-control {
    margin: 15px;
  }

  .ck-content {
    height: 250px;
    margin-left: auto;
    margin-right: auto;
    text-align: initial;
  }

</style>
