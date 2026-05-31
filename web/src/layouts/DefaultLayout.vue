<template>
  <Header />
  <main class="mt-14">
    <RouterView />
  </main>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
</script>
