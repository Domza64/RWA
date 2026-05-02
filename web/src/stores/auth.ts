import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api, ApiError } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(true)
  const isAuthenticated = computed(() => !!accessToken.value)
  const accessToken = ref(localStorage.getItem('access_token') || null)

  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    localStorage.setItem('access_token', access)
    if (refresh) localStorage.setItem('refresh_token', refresh)
  }

  async function fetchMe() {
    if (!accessToken.value) return

    try {
      loading.value = true
      const data = await api.get('/auth/me')
      user.value = data
      return data
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) logout()
      throw error
    } finally {
      loading.value = false
    }
  }

  async function initAuth() {
    await fetchMe()
    loading.value = false
  }

  async function login(username: string, password: string) {
    const response = await api.post('/auth/login', { username, password })
    setTokens(response.access_token, response.refresh_token)
    await fetchMe()
    return user.value
  }

  async function register(username: string, email: string, password: string) {
    await api.post('/auth/register', { username, email, password })
  }

  function logout() {
    user.value = null
    accessToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    import('@/router').then(({ default: router }) => router.push('/login'))
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    loading,
    setTokens,
    fetchMe,
    login,
    register,
    logout,
    initAuth,
  }
})
