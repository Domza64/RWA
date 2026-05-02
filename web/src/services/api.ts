const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function getToken(): string | null {
  return localStorage.getItem('access_token')
}

let isRefreshing = false
let requestQueue: {
  resolve: (token: string | null) => void
  reject: (error: unknown) => void
}[] = []

function processQueue(error: unknown, token: string | null = null): void {
  requestQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error)
    else resolve(token)
  })
  requestQueue = []
}

function buildHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }

  const token = getToken()

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  return headers
}

async function tryRefresh(): Promise<string> {
  const refreshToken = localStorage.getItem('refresh_token')

  if (!refreshToken) {
    throw new Error('No refresh token available')
  }

  const response = await fetch(`${BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })

  if (!response.ok) {
    throw new Error('Token refresh failed')
  }

  const data = await response.json()

  localStorage.setItem('access_token', data.access_token)

  if (data.refresh_token) {
    localStorage.setItem('refresh_token', data.refresh_token)
  }

  return data.access_token
}

async function logoutUser(): Promise<void> {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')

  const { default: router } = await import('@/router')
  router.push('/login')
}

async function handleResponse(response: Response): Promise<any> {
  if (response.status === 204) return null

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const message = data?.message || `HTTP error ${response.status}`
    const code = data?.code || 'unknown_error'

    throw new ApiError(message, response.status, code)
  }

  return data
}

async function request(method: string, path: string, body: any = null): Promise<any> {
  const url = `${BASE_URL}${path}`

  const options: RequestInit = {
    method,
    headers: buildHeaders(),
  }

  if (body !== null) {
    options.body = JSON.stringify(body)
  }

  let response = await fetch(url, options)

  if (response.status === 401) {
    if (isRefreshing) {
      return new Promise<string | null>((resolve, reject) => {
        requestQueue.push({ resolve, reject })
      }).then(async (newToken) => {
        ;(options.headers as Record<string, string>)['Authorization'] = `Bearer ${newToken}`

        return handleResponse(await fetch(url, options))
      })
    }

    isRefreshing = true

    try {
      const newToken = await tryRefresh()

      processQueue(null, newToken)
      ;(options.headers as Record<string, string>)['Authorization'] = `Bearer ${newToken}`

      response = await fetch(url, options)
    } catch (error) {
      processQueue(error, null)

      await logoutUser()

      throw new ApiError('Session expired. Please log in again.', 401, 'session_expired')
    } finally {
      isRefreshing = false
    }
  }

  return handleResponse(response)
}

export class ApiError extends Error {
  status: number
  code: string

  constructor(message: string, status: number, code: string) {
    super(message)

    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}

export const api = {
  get: (path: string) => request('GET', path),
  post: (path: string, body: any) => request('POST', path, body),
  patch: (path: string, body: any) => request('PATCH', path, body),
  delete: (path: string) => request('DELETE', path),
}
