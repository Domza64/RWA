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
  <section class="grid grid-cols-[5fr_1fr] h-full w-full overflow-hidden">
    <!-- Main content -->
    <div class="flex flex-col h-full overflow-hidden p-6">
      <!-- Board header -->
      <div class="shrink-0 border-b-4 border-black pb-6 mb-6">
        <!-- Loading skeleton -->
        <div v-if="loading" class="space-y-3">
          <div class="h-10 w-64 bg-yellow-400 border-4 border-black animate-pulse"></div>
          <div class="h-4 w-96 bg-gray-300 border-2 border-black animate-pulse"></div>
        </div>

        <div v-else-if="board" class="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h1 class="text-4xl font-black uppercase tracking-tight text-black">
              {{ board.name }}
            </h1>
            <p class="mt-2 font-bold text-gray-700">
              {{ board.description }}
            </p>
          </div>

          <div class="flex gap-3 shrink-0">
            <RouterLink
              :to="`/boards/${boardId}/create-stage`"
              class="border-4 border-black bg-white text-black font-black uppercase tracking-wider px-4 py-2 hover:bg-yellow-400 transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 text-sm"
            >
              + Stage
            </RouterLink>
            <RouterLink
              :to="`/boards/${boardId}/create`"
              class="border-4 border-black bg-indigo-600 text-white font-black uppercase tracking-wider px-4 py-2 hover:bg-black transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 text-sm"
            >
              + Ticket
            </RouterLink>
          </div>
        </div>

        <div v-else class="font-black uppercase text-black border-4 border-black p-4 bg-yellow-400 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">Board not found.</div>
      </div>

      <!-- Tickets area -->
      <div class="flex-1 overflow-hidden">
        <TicketPanel />
        <RouterView />
      </div>
    </div>

    <!-- Members sidebar -->
    <aside class="h-full overflow-y-auto border-l-4 border-black pl-4 py-6 pr-2">
      <h2 class="text-xl font-black uppercase tracking-widest border-b-4 border-black pb-3 mb-6">Members</h2>
      <MembersPanel />
    </aside>
  </section>
</template>
