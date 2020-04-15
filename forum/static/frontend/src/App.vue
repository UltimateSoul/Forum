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
                :type="getNotificationType(notification.type)"
                :key="notification.id">
                {{ notification.message }}
              </v-alert>
            </div>
            <transition name="slide" mode="out-in">
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
        notifications: []
      }
    },
    created() {
      let token = sessionStorage.getItem('auth_token');
      if (Boolean(token)) {
        const vueInstance = this
        this.$store.commit('setAuthToken');
        this.$store.dispatch('fetchUser').then(
          () => {
            vueInstance.getNotifications()
          }
        )
      } else {
        this.$router.push(
          {name: 'login'}
        )
      }

    },
    methods: {
      getNotifications() {
        axios.get('http://0.0.0.0:5000/core/notifications-list/').then(
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
        axios.delete(`http://0.0.0.0:5000/core/delete-notification/${notificationID}/`).then(
          (response) => {
            switch (response.status) {
              case 204:
                this.getNotifications()
            }
          }
        )
      },
      getNotificationType(notificationTypeNumber) {
        let notificationType = 'success'
        switch (notificationTypeNumber) {
          case 1:
            notificationType = 'success';
            break;
          case 2:
            notificationType = 'info';
            break;
          case 3:
            notificationType = 'warning';
            break;
          case 4:
            notificationType = 'error';
            break;
        }
        return notificationType
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

  .clickable {
    cursor: pointer;
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

  .slide-enter {
    opacity: 0;
  }

  .slide-enter-active {
    animation: slide-in 1s ease-out forwards;
    transition: opacity 1s;
  }

  .slide-leave {

  }

  .slide-leave-active {
    animation: slide-out 1s ease-out forwards;
    transition: opacity 1s;
    opacity: 0;
  }

  @keyframes slide-in {
    from {
      transform: translateY(20px);
    }
    to {
      transform: translateY(0);
    }
  }

  @keyframes slide-out {
    from {
      transform: translateY(0);
    }
    to {
      transform: translateY(20px);
    }
  }
</style>
