<script setup lang="ts">
import { useNotificationStore } from '@/stores/notification'
import NotificationCard from './NotificationCard.vue'

const store = useNotificationStore()
</script>

<template>
  <Teleport to="body">
    <div class="fixed bottom-4 right-4 z-50 flex w-full max-w-sm flex-col">
      <TransitionGroup name="notification">
        <NotificationCard v-for="n in store.data" :key="n.id" :notification="n" />
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.25s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* important for smooth movement */
.notification-move {
  transition: transform 0.25s ease;
}
</style>
