<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getBoardTickets } from '@/services/tickets'
import { getWorkflowStages } from '@/services/boards'
import type { SimpleTicket, WorkflowStage } from '@/types/ticket'
import { useNotificationStore } from '@/stores/notification'
import TicketCard from '@/components/ui/cards/TicketCard.vue'
import { useTicketEventsStore } from '@/stores/ticketEvents'

const notificationStore = useNotificationStore()
const ticketEventsStore = useTicketEventsStore()
const boardId = parseInt(useRoute().params.board_id as string)

const loading = ref(true)

const workflowStages = ref<WorkflowStage[]>([])
const tickets = ref<SimpleTicket[]>([])

async function load(): Promise<void> {
  loading.value = true

  try {
    const [stages, boardTickets] = await Promise.all([
      getWorkflowStages(boardId),
      getBoardTickets(boardId),
    ])

    workflowStages.value = stages
    tickets.value = boardTickets
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Error loading board data...')
  } finally {
    loading.value = false
  }
}

onMounted(load)

watch(
  () => ticketEventsStore.refreshCounter,
  () => {
    load()
  },
)

const groupedTickets = computed(() => {
  const map = new Map<number, SimpleTicket[]>()

  for (const stage of workflowStages.value) {
    map.set(stage.stage_id, [])
  }

  for (const ticket of tickets.value) {
    if (!ticket.current_stage) continue
    const arr = map.get(ticket.current_stage.stage_id)
    if (arr) arr.push(ticket)
  }

  return workflowStages.value.map((stage) => ({
    stage,
    tickets: map.get(stage.stage_id) ?? [],
  }))
})
</script>

<template>
  <div v-if="loading" class="font-black uppercase text-xl tracking-widest animate-pulse p-4 bg-yellow-400 border-4 border-black inline-block shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
    Loading...
  </div>

  <div v-else-if="groupedTickets.length === 0" class="border-4 border-black p-6 bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] font-black uppercase text-center">
    No stages yet. Create one to get started.
  </div>

  <div v-else class="flex gap-6 h-full overflow-x-auto pb-4">
    <div
      v-for="col in groupedTickets"
      :key="col.stage.stage_id"
      class="min-w-[260px] w-[260px] flex flex-col border-4 border-black bg-white shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]"
    >
      <!-- Column header -->
      <div class="p-3 border-b-4 border-black bg-indigo-600 text-white">
        <h3 class="font-black uppercase tracking-wider text-sm line-clamp-1">
          {{ col.stage.name }}
        </h3>
        <p class="text-xs font-bold opacity-80 mt-0.5">{{ col.tickets.length }} ticket{{ col.tickets.length !== 1 ? 's' : '' }}</p>
      </div>

      <!-- Tickets -->
      <div class="p-3 flex flex-col gap-3 overflow-y-auto flex-1">
        <RouterLink
          v-for="ticket in col.tickets"
          :key="ticket.ticket_id"
          :to="`/boards/${boardId}/tickets/${ticket.ticket_id}`"
        >
          <TicketCard :data="ticket" />
        </RouterLink>

        <div v-if="col.tickets.length === 0" class="text-xs font-black uppercase text-gray-400 p-2 border-2 border-dashed border-gray-300 text-center">
          Empty
        </div>
      </div>
    </div>
  </div>
</template>
