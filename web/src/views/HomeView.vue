<template>
  <main class="min-h-screen bg-gray-100 p-4 md:p-8 flex flex-col gap-12 font-medium">
    <!-- Hero Section -->
    <section
      class="max-w-5xl mx-auto w-full mt-4 md:mt-12 bg-white border-4 border-black shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] p-8 md:p-16 flex flex-col md:flex-row items-center gap-8"
    >
      <div class="flex-1 text-left">
        <div
          class="inline-block bg-yellow-400 text-black font-black uppercase px-3 py-1 border-2 border-black mb-4 tracking-wider text-sm"
        >
          Now with 50% more bugs!
        </div>
        <h1 class="text-5xl md:text-7xl font-black uppercase tracking-tighter leading-none mb-6">
          Jira 2
        </h1>
        <p class="text-xl md:text-2xl font-bold mb-8 max-w-lg border-l-4 border-black pl-4">
          It's like Jira, but objectively worse in every measurable way. Don't expect much and you
          still might be disappointed.
        </p>
        <div class="flex flex-wrap gap-4">
          <RouterLink
            to="/register"
            class="bg-indigo-600 text-white border-4 border-black font-black uppercase tracking-wider px-8 py-4 hover:bg-black hover:text-white active:translate-x-1 active:translate-y-1 transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:shadow-none"
          >
            Sign Up (Please don't)
          </RouterLink>
          <RouterLink
            to="/login"
            class="bg-white text-black border-4 border-black font-black uppercase tracking-wider px-8 py-4 hover:bg-yellow-400 transition-colors shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
          >
            Log In
          </RouterLink>
        </div>
      </div>

      <!-- Image Placeholder -->
      <div
        class="flex-1 w-full bg-gray-200 border-4 border-black aspect-video flex items-center justify-center p-4 text-center shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] bg-indigo-100"
      >
        <div class="font-black uppercase text-gray-500">
          [ TODO: Image of a barely functional kanban board. ]
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="max-w-5xl mx-auto w-full grid grid-cols-1 md:grid-cols-3 gap-8">
      <div
        class="bg-indigo-600 text-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
      >
        <h3 class="text-2xl font-black uppercase border-b-4 border-black pb-2 mb-4">Tickets</h3>
        <p class="font-bold text-lg">
          You can make tickets. You can even drag them. Will they stay there? Who knows! The
          suspense is a feature.
        </p>
      </div>

      <div
        class="bg-yellow-400 text-black border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
      >
        <h3 class="text-2xl font-black uppercase border-b-4 border-black pb-2 mb-4">Users</h3>
        <p class="font-bold text-lg">
          Add your teammates! Then blame them when the site crashes. We don't have an activity log,
          so no one can prove anything.
        </p>
      </div>

      <div
        class="bg-white text-black border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
      >
        <h3 class="text-2xl font-black uppercase border-b-4 border-black pb-2 mb-4">Analytics</h3>
        <p class="font-bold text-lg">
          Just kidding. We don't track anything. Not because of privacy, but because it takes time
          to implement.
        </p>
      </div>
    </section>

    <!-- Footer CTA Placeholder -->
    <section
      class="max-w-5xl mx-auto w-full mb-12 bg-white border-4 border-black p-8 text-center shadow-[12px_12px_0px_0px_rgba(0,0,0,1)]"
    >
      <h2 class="text-4xl font-black uppercase mb-4">Still scrolling?</h2>
      <p class="text-xl font-bold mb-6">
        Honestly, that's more commitment than we put into the backend. Here's another image for you.
      </p>
      <div
        class="w-full max-w-2xl mx-auto bg-gray-200 border-4 border-black h-48 flex items-center justify-center text-center shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
      >
        <span class="font-black uppercase text-gray-500 px-4">[ TODO: Add some image here. ]</span>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
