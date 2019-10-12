import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
const Login = resolve => {
  require.ensure(['@/components/Login'], () => {
    resolve(require('@/components/Login'))
  })
};
const Conversation = resolve => {
  require.ensure(['@/components/Conversation'], () => {
    resolve(require('@/components/Conversation'))
  })
};
const TopicCreation = resolve => {
  require.ensure(['@/components/TopicCreation'], () => {
    resolve(require('@/components/TopicCreation'))
  })
};
const Shop = resolve => {
  require.ensure(['@/components/Shop'], () => {
    resolve(require('@/components/Shop'))
  })
};
const GetStarted = resolve => {
  require.ensure(['@/components/GetStarted'], () => {
    resolve(require('@/components/GetStarted'))
  })
};
const UserProfile = resolve => {
  require.ensure(['@/components/UserProfile'], () => {
    resolve(require('@/components/UserProfile'))
  })
};

Vue.use(Router);

export default new Router({
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return {selector: to.hash};
    }
    return {x: 0,
            y: 0}
  },
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
      name: 'get-started',
      component: GetStarted
    },
    {
      path: '/user-profile/:id',
      name: 'user-profile',
      component: UserProfile
    },
    {
      path: '*',
      redirect: {name: 'home'}
    }
  ],
  mode: 'history'
})
