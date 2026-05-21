<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Notifications from '@/components/notifications/Notifications.vue'

const auth = useAuthStore()

onMounted(() => {
  auth.initAuth()
})
</script>

<template>
  <DefaultLayout />
  <Notifications />
</template>
