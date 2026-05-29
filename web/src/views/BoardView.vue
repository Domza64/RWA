<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getBoard, getMembers } from '@/services/boards'
import { getBoardTickets } from '@/services/tickets'
import type { Board, Member } from '@/types/board'
import { useNotificationStore } from '@/stores/notification'
import type { SimpleTicketResponse } from '@/types/ticket'

const notificationStore = useNotificationStore()
const boardId = parseInt(useRoute().params.board_id as string)
const loading = ref(true)
const board = ref<Board | null>(null)
const members = ref<Member[]>([])
const tickets = ref<SimpleTicketResponse[]>([])

async function loadData(): Promise<void> {
  loading.value = true
  try {
    board.value = await getBoard(boardId)
    members.value = await getMembers(boardId)
    tickets.value = await getBoardTickets(boardId)
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Greška pri dohvatu.')
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <section class="grid grid-cols-[2fr_10fr_3fr] gap-4 h-full">
    <div class="bg-gray-300">My boards... load from pinia store</div>

    <div>
      <div v-if="loading">Loading...</div>
      <div v-else-if="board">
        <h1>{{ board.name }}</h1>
        <p>{{ board.description }}</p>
        <div>
          <h2>Tickets</h2>
          <div>
            {{ tickets }}
          </div>
        </div>
      </div>
      <div v-else>Board not found.</div>
    </div>
    <div class="bg-gray-300">{{ members }}</div>
  </section>
</template>
