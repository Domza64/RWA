<script setup lang="ts">
import RegisterForm from '@/components/RegisterForm.vue'
</script>

<template>
  <section class="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] w-full px-4 bg-gray-100">
    <div class="w-full max-w-md border-4 border-black p-8 bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
      <h1 class="text-4xl font-black uppercase mb-8 text-center tracking-tight border-b-4 border-black pb-4">Register</h1>
      <RegisterForm />
    </div>
  </section>
</template>
