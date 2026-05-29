<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getBoardTickets } from '@/services/tickets'
import { getWorkflowStages } from '@/services/boards'
import type { SimpleTicket, WorkflowStage } from '@/types/ticket'
import { useNotificationStore } from '@/stores/notification'
import TicketCard from '@/components/ui/cards/TicketCard.vue'

const notificationStore = useNotificationStore()
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

const groupedTickets = computed(() => {
  const map = new Map<number, SimpleTicket[]>()

  for (const stage of workflowStages.value) {
    map.set(stage.stage_id, [])
  }

  for (const ticket of tickets.value) {
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
  <div v-if="loading" class="text-gray-600">Loading board...</div>

  <div v-else class="flex gap-4 h-full overflow-x-auto">
    <div
      v-for="col in groupedTickets"
      :key="col.stage.stage_id"
      class="min-w-[250px] flex flex-col border border-gray-300 rounded-md"
    >
      <!-- Column header -->
      <div class="p-2 border-b border-gray-300">
        <h3 class="text-gray-700 font-semibold">
          {{ col.stage.name }}
        </h3>
        <p class="text-xs text-gray-400">{{ col.tickets.length }} tickets</p>
      </div>

      <!-- Tickets -->
      <div class="p-2 flex flex-col gap-2 overflow-y-auto">
        <div v-for="ticket in col.tickets" :key="ticket.ticket_id">
          <RouterLink :to="`/boards/${boardId}/tickets/${ticket.ticket_id}`">
            <TicketCard :data="ticket" />
          </RouterLink>
        </div>

        <div v-if="col.tickets.length === 0" class="text-xs text-gray-300 p-2">No tickets</div>
      </div>
    </div>
  </div>
</template>
