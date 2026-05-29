<template>
  <header class="bg-indigo-800 text-white">
    <nav class="mx-auto max-w-7xl w-full flex justify-between">
      <div>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/boards">Boards</RouterLink>
      </div>

      <div v-if="authStore.loading">Loading...</div>
      <RouterLink v-else-if="!authStore.isAuthenticated" to="/login"> Login </RouterLink>

      <div v-else class="flex gap-4">
        <span>{{ authStore.user.username }}</span>
        <button @click="authStore.logout()">Logout</button>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>
