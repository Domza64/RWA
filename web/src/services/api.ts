import axios from 'axios'
import type { BackendError } from '@/types/api'

export class ApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.set('Authorization', `Bearer ${token}`)
  return config
})

let refreshingToken: Promise<void> | null = null

api.interceptors.response.use(
  (response) => response,
  async (error: unknown) => {
    if (!axios.isAxiosError(error) || !error.response) throw error

    const status = error.response.status
    const data = error.response.data as Partial<BackendError>

    // login/refresh or if status code is not 401, retry shouldnt be trigger
    const url = error.config?.url ?? ''
    const isAuthEndpoint = url.includes('/auth/login') || url.includes('/auth/refresh')
    if (status !== 401 || isAuthEndpoint) {
      throw new ApiError(data.code ?? 'unknown_error', data.message ?? error.message, status)
    }

    const refreshToken = localStorage.getItem('refresh_token')

    if (!refreshToken) {
      throw new ApiError('unauthenticated', 'Not authenticated', 401)
    }

    // 401 on endpoint that requires auth, try to refresh token
    try {
      if (!refreshingToken) {
        // Dynamic import to not get circular dependency with auth store
        const { useAuthStore } = await import('@/stores/auth')
        refreshingToken = useAuthStore()
          .refreshToken()
          .finally(() => {
            refreshingToken = null
          })
      }
      await refreshingToken

      return api.request(error.config!)
    } catch {
      const { useAuthStore } = await import('@/stores/auth')
      useAuthStore().logout()
      throw new ApiError('session_expired', 'Session expired', 401)
    }
  },
)
