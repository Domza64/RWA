<template>
  <header class="bg-green-800 text-white">
    <nav class="mx-auto max-w-7xl w-full flex justify-between">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/login">Login</RouterLink>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
