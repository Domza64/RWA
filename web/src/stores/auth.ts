import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TokenResponse } from '@/types/auth'
import type { UserData } from '@/types/user'
import { api } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserData | null>(null)
  const loading = ref(true)
  const isAuthenticated = ref(false) // computed(() => !!accessToken.value && user != null)
  const accessToken = ref(localStorage.getItem('access_token') || null)

  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    localStorage.setItem('access_token', access)
    if (refresh) localStorage.setItem('refresh_token', refresh)
  }

  async function fetchMe() {
    const { data } = await api.get<UserData>('/auth/me')
    user.value = data
  }

  async function refreshToken(): Promise<void> {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) throw new Error('No refresh token')
    const { data } = await api.post<TokenResponse>(
      '/auth/refresh',
      { refresh_token: refreshToken },
      { headers: { Authorization: '' } },
    )
    accessToken.value = data.access_token
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
  }

  async function initAuth() {
    try {
      if (!accessToken.value) {
        return
      }
      await fetchMe()
      isAuthenticated.value = true
    } catch {
      logout()
      isAuthenticated.value = false
    } finally {
      loading.value = false
    }
  }

  async function login(username: string, password: string) {
    const { data } = await api.post<TokenResponse>('/auth/login', { username, password })
    setTokens(data.access_token, data.refresh_token)
    await fetchMe()
    isAuthenticated.value = true
    return user.value
  }

  async function register(username: string, email: string, password: string) {
    await api.post('/auth/register', { username, email, password })
  }

  function logout() {
    user.value = null
    accessToken.value = null
    isAuthenticated.value = false
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
    refreshToken,
    login,
    register,
    logout,
    initAuth,
  }
})
