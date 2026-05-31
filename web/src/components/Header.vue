<template>
  <header class="bg-indigo-600 text-white fixed top-0 w-full h-14 border-b-4 border-black z-50">
    <nav class="mx-auto max-w-7xl w-full flex justify-between items-center h-full px-4 font-black uppercase tracking-wider text-sm">
      <div class="flex gap-6 h-full items-center">
        <RouterLink to="/" class="hover:bg-white hover:text-black px-3 py-1 border-2 border-transparent hover:border-black transition-colors">Home</RouterLink>
        <RouterLink to="/boards" class="hover:bg-white hover:text-black px-3 py-1 border-2 border-transparent hover:border-black transition-colors">Boards</RouterLink>
      </div>

      <div v-if="authStore.loading" class="animate-pulse">LOADING...</div>
      <RouterLink v-else-if="!authStore.isAuthenticated" to="/login" class="bg-white text-black hover:bg-black hover:text-white px-4 py-1 border-2 border-black transition-colors">LOGIN</RouterLink>

      <div v-else class="flex gap-4 items-center h-full">
        <span class="bg-white text-black px-3 py-1 border-2 border-black">{{ authStore.user.username }}</span>
        <button @click="authStore.logout()" class="bg-black text-white hover:bg-white hover:text-black px-3 py-1 border-2 border-black transition-colors">LOGOUT</button>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>
