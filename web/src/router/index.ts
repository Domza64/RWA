import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import HomeView from '../views/HomeView.vue'
import { useUiStore } from '@/stores/ui.ts'

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
      component: () => import('../layouts/BoardLayout.vue'),
      children: [
        {
          path: '',
          name: 'boards',
          component: () => import('../views/BoardsView.vue'),
        },
        {
          path: 'create',
          name: 'create',
          component: () => import('../views/BoardCreateView.vue'),
        },
        {
          path: ':board_id',
          name: 'board',
          component: () => import('../views/BoardView.vue'),
          children: [
            {
              path: 'create',
              name: 'create-ticket',
              component: () => import('../views/TicketCreateView.vue'),
            },
            {
              path: 'create-stage',
              name: 'create-stage',
              component: () => import('../views/StageCreateView.vue'),
            },
          ],
        },
        {
          path: ':board_id/tickets/:ticket_id',
          name: 'ticket',
          component: () => import('../views/TicketView.vue'),
        },
      ],
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
  const ui = useUiStore()

  ui.loading = true

  const publicRoutes = ['login', 'register', '']
  const authPages = ['login', 'register']

  const currentRoute: string = to.name?.toString() || ''

  if (authPages.includes(currentRoute) && authStore.user) {
    return { name: 'boards' }
  }

  if (!publicRoutes.includes(currentRoute) && !authStore.user && !authStore.loading) {
    return { name: 'login' }
  }
})

router.afterEach(() => {
  const ui = useUiStore()
  ui.loading = false
})

router.onError(() => {
  const ui = useUiStore()
  ui.loading = false
})

export default router
