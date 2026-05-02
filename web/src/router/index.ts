import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      component: HomeView,
    },
    {
      path: '/boards',
      name: 'boards',
      component: () => import('../views/BoardsView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  const publicRoutes = ['login', 'register', '']

  const currentRoute: string = to.name?.toString() || ''
  console.log(currentRoute)

  if (!publicRoutes.includes(currentRoute) && !authStore.user) {
    return { name: 'login' }
  }
})

export default router
