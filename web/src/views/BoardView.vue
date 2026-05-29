<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getBoard } from '@/services/boards'
import { getBoardTickets } from '@/services/tickets'
import type { Board, Member } from '@/types/board'
import { useNotificationStore } from '@/stores/notification'
import type { SimpleTicketResponse } from '@/types/ticket'
import { useBoardStore } from '@/stores/board'
import MembersPanel from '@/components/MembersPanel.vue'

const notificationStore = useNotificationStore()

const boardId = parseInt(useRoute().params.board_id as string)
const loading = ref(true)
const board = ref<Board | null>(null)
const tickets = ref<SimpleTicketResponse[]>([])

async function loadData(): Promise<void> {
  loading.value = true
  try {
    board.value = await getBoard(boardId)
    tickets.value = await getBoardTickets(boardId)
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Error getting data...')
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <section class="grid grid-cols-[5fr_1fr] gap-4 h-full w-full overflow-hidden">
    <div class="overflow-hidden flex flex-col h-full">
      <div v-if="loading">Loading...</div>
      <div v-else-if="board" class="flex flex-col h-full overflow-hidden">
        <h1 class="shrink-0">{{ board.name }}</h1>
        <p class="shrink-0">{{ board.description }}</p>
        <div class="flex-1 overflow-hidden flex flex-col">
          <h2 class="shrink-0">Tickets</h2>
          <RouterLink class="shrink-0" :to="`/boards/${boardId}/create`">Create ticket</RouterLink>
          <div class="flex-1 overflow-hidden">
            <div v-for="ticket in tickets" :key="ticket.ticket_id">
              <RouterLink :to="`/boards/${boardId}/tickets/${ticket.ticket_id}`">{{
                ticket.title
              }}</RouterLink>
            </div>
            <RouterView />
          </div>
        </div>
      </div>
      <div v-else>Board not found.</div>
    </div>
    <div class="overflow-y-auto h-full"><MembersPanel /></div>
  </section>
</template>
