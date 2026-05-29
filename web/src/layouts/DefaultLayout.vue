<template>
  <Header />
  <main class="mt-10">
    <RouterView />
  </main>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
</script>
