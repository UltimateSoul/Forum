import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/pages/Home'
const Login = resolve => {
  require.ensure(['@/components/pages/Login'], () => {
    resolve(require('@/components/pages/Login'))
  })
};
const Conversation = resolve => {
  require.ensure(['@/components/pages/Conversation'], () => {
    resolve(require('@/components/pages/Conversation'))
  })
};
const TopicCreation = resolve => {
  require.ensure(['@/components/pages/TopicCreation'], () => {
    resolve(require('@/components/pages/TopicCreation'))
  })
};
const Shop = resolve => {
  require.ensure(['@/components/pages/Shop'], () => {
    resolve(require('@/components/pages/Shop'))
  })
};
const GetStarted = resolve => {
  require.ensure(['@/components/pages/GetStarted'], () => {
    resolve(require('@/components/pages/GetStarted'))
  })
};
const UserProfile = resolve => {
  require.ensure(['@/components/pages/UserProfile'], () => {
    resolve(require('@/components/pages/UserProfile'))
  })
};
const Sections = resolve => {
  require.ensure(['@/components/pages/Sections'], () => {
    resolve(require('@/components/pages/Sections'))
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
      path: '/conversation/:section',
      name: 'conversation',
      component: Conversation
    },
    {
      path: '/topic-creation/:section',
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
      path: '/sections',
      name: 'sections',
      component: Sections
    },
    {
      path: '*',
      redirect: {name: 'home'}
    }
  ],
  mode: 'history'
})
