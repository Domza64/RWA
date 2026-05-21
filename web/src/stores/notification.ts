import { defineStore } from 'pinia'
import { ref } from 'vue'

export type NotificationType = 'success' | 'error' | 'info'

export interface Notification {
  id: number
  message: string
  type: NotificationType
}

let id_cnt = 0

export const useNotificationStore = defineStore('notifications', () => {
  const data = ref<Notification[]>([])

  function add(message: string, type: NotificationType = 'info'): void {
    const id = ++id_cnt
    data.value.push({ id, message, type })
    setTimeout(() => remove(id), 4000)
  }

  function remove(id: number): void {
    data.value = data.value.filter((o) => o.id !== id)
  }

  return {
    data,
    remove: (id: number) => remove(id),
    success: (message: string) => add(message, 'success'),
    error: (message: string) => add(message, 'error'),
    info: (message: string) => add(message, 'info'),
  }
})
