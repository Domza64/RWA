<template>
  <Header />
  <main class="h-screen w-full">
    <RouterView />
  </main>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
</script>
