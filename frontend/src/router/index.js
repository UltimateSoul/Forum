import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/pages/Home'

const Login = resolve => {
  require.ensure(['@/components/pages/authentication/Login'], () => {
    resolve(require('@/components/pages/authentication/Login'))
  })
};
const Conversation = resolve => {
  require.ensure(['@/components/pages/Conversation'], () => {
    resolve(require('@/components/pages/Conversation'))
  })
};
const TopicCreation = resolve => {
  require.ensure(['@/components/pages/topic/TopicCreation'], () => {
    resolve(require('@/components/pages/topic/TopicCreation'))
  })
};
const TopicEditing = resolve => {
  require.ensure(['@/components/pages/topic/TopicEditing'], () => {
    resolve(require('@/components/pages/topic/TopicEditing'))
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
const Registration = resolve => {
  require.ensure(['@/components/pages/authentication/Registration'], () => {
    resolve(require('@/components/pages/authentication/Registration'))
  })
};
const Topic = resolve => {
  require.ensure(['@/components/pages/topic/Topic'], () => {
    resolve(require('@/components/pages/topic/Topic'))
  })
};
const Teams = resolve => {
  require.ensure(['@/components/pages/team/Teams'], () => {
    resolve(require('@/components/pages/team/Teams'))
  })
};
const Team = resolve => {
  require.ensure(['@/components/pages/team/Team'], () => {
    resolve(require('@/components/pages/team/Team'))
  })
};
const CreateTeam = resolve => {
  require.ensure(['@/components/pages/team/CreateTeam'], () => {
    resolve(require('@/components/pages/team/CreateTeam'))
  })
};
const EditTeam = resolve => {
  require.ensure(['@/components/pages/team/EditTeam'], () => {
    resolve(require('@/components/pages/team/EditTeam'))
  })
};
const ManageTeamMembers = resolve => {
  require.ensure(['@/components/pages/team/ManageTeamMembers'], () => {
    resolve(require('@/components/pages/team/ManageTeamMembers'))
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
      path: '/conversation/:section/topic/:topicID',
      name: 'topic',
      component: Topic
    },
    {
      path: '/topic-creation/:section',
      name: 'topic-creation',
      component: TopicCreation
    },
    {
      path: '/topic-editing/:section/:topicID',
      name: 'topic-editing',
      component: TopicEditing
    },
    {
      path: '/shop',
      name: 'shop',
      component: Shop
    },
    {
      path: '/teams',
      name: 'teams',
      component: Teams
    },
    {
      path: '/teams/:teamID',
      name: 'team',
      component: Team
    },
    {
      path: '/teams/manage-team-members',
      name: 'manage-team-members',
      component: ManageTeamMembers
    },
    {
      path: '/edit-team/',
      name: 'edit-team',
      component: EditTeam
    },
    {
      path: '/create-team',
      name: 'create-team',
      component: CreateTeam
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
      path: '/registration',
      name: 'registration',
      component: Registration
    },
    // {
    //   path: '*',
    //   redirect: {name: 'home'}
    // }
  ],
  mode: 'history'
})
