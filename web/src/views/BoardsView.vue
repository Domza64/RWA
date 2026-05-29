<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Board } from '@/types/board'
import { useNotificationStore } from '@/stores/notification'
import { getBoards } from '@/services/boards'
import BoardCard from '@/components/ui/cards/BoardCard.vue'

const notificationStore = useNotificationStore()
const boards = ref<Board[]>([])
const loading = ref<boolean>(true)

async function loadData(): Promise<void> {
  loading.value = true
  try {
    const data = await getBoards()
    boards.value = data
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Greška pri dohvatu.')
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <section class="text-center my-24">
    <h1 class="text-4xl font-bold">Your boards</h1>
    <p v-if="loading">Loading...</p>
    <div v-else-if="boards.length === 0">
      <p>No boards found.</p>
    </div>
    <div v-else class="flex gap-2 mx-auto my-4 w-fit">
      <RouterLink v-for="board in boards" :key="board.board_id" :to="`/boards/${board.board_id}`">
        <BoardCard :data="board" />
      </RouterLink>
    </div>
    <RouterLink to="/boards/create">Create a new board</RouterLink>
  </section>
</template>
