<script setup lang="ts">
import type { Notification } from '@/stores/notification'
import { useNotificationStore } from '@/stores/notification'

const props = defineProps<{ notification: Notification }>()
const store = useNotificationStore()

const styles = {
  success: 'border-indigo-500 bg-indigo-50 text-indigo-800',
  error: 'border-red-500 bg-red-100 text-red-800',
  info: 'border-blue-500 bg-blue-50 text-blue-800',
}
</script>

<template>
  <div
    @click="store.remove(props.notification.id)"
    class="mb-3 flex min-w-[320px] items-center justify-between gap-4 border rounded px-4 py-3 shadow cursor-pointer"
    :class="styles[props.notification.type]"
  >
    <span class="text-sm font-medium">
      {{ props.notification.message }}
    </span>

    <button class="text-lg">×</button>
  </div>
</template>
