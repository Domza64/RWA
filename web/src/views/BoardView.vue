<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getBoard } from '@/services/boards'
import type { Board } from '@/types/board'
import { useNotificationStore } from '@/stores/notification'
import TicketPanel from '@/components/TicketPanel.vue'
import MembersPanel from '@/components/MembersPanel.vue'

const notificationStore = useNotificationStore()

const boardId = parseInt(useRoute().params.board_id as string)
const loading = ref(true)
const board = ref<Board | null>(null)

async function load(): Promise<void> {
  loading.value = true
  try {
    board.value = await getBoard(boardId)
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Error getting data...')
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section class="grid grid-cols-[5fr_1fr] gap-4 h-full w-full overflow-hidden">
    <!-- Main content -->
    <div class="flex flex-col h-full overflow-hidden p-3">
      <!-- Board header -->
      <div class="shrink-0 border-b border-gray-300 pb-4 mb-4">
        <div v-if="loading" class="space-y-2">
          <div class="h-8 w-48 bg-gray-100 rounded animate-pulse"></div>
          <div class="h-4 w-96 bg-gray-50 rounded animate-pulse"></div>
        </div>

        <div v-else-if="board">
          <h1 class="text-3xl font-bold text-gray-700">
            {{ board.name }}
          </h1>

          <p class="mt-2 text-sm text-gray-500">
            {{ board.description }}
          </p>
        </div>

        <div v-else class="text-gray-600 font-medium">Board not found.</div>
      </div>

      <!-- Tickets -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <div class="shrink-0 flex items-center justify-between border-b border-gray-300 pb-3 mb-3">
          <h2 class="text-xl font-semibold text-gray-700">Tickets</h2>

          <div class="flex gap-2">
            <RouterLink
              :to="`/boards/${boardId}/create-stage`"
              class="px-3 py-2 rounded-md bg-indigo-100 text-indigo-700 hover:bg-indigo-200 text-sm font-medium"
            >
              Create stage
            </RouterLink>
            <RouterLink
              :to="`/boards/${boardId}/create`"
              class="px-3 py-2 rounded-md bg-indigo-600 text-white hover:bg-indigo-700 text-sm font-medium"
            >
              Create ticket
            </RouterLink>
          </div>
        </div>

        <div class="flex-1 overflow-hidden">
          <TicketPanel />
          <RouterView />
        </div>
      </div>
    </div>

    <!-- Members -->
    <aside class="h-full overflow-y-auto border-l border-gray-300 pl-4">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Members</h2>

      <MembersPanel />
    </aside>
  </section>
</template>
