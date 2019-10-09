import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Conversation from '@/components/Conversation'
import TopicCreation from '@/components/TopicCreation'
import Shop from '@/components/Shop'
import GetStarted from '@/components/GetStarted'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/conversation',
      name: 'conversation',
      component: Conversation
    },
    {
      path: '/topic-creation',
      name: 'topic-creation',
      component: TopicCreation
    },
    {
      path: '/shop',
      name: 'shop',
      component: Shop
    },
    {
      path: '/get-started',
      name: 'Get Started',
      component: GetStarted
    }
  ],
  mode: 'history'
})
