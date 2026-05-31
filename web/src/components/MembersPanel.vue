<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getMembers } from '@/services/boards'
import type { Member } from '@/types/board'
import { useNotificationStore } from '@/stores/notification'

const notificationStore = useNotificationStore()

const boardId = parseInt(useRoute().params.board_id as string)
const loading = ref(true)
const members = ref<Member[]>([])

async function load(): Promise<void> {
  loading.value = true
  try {
    members.value = await getMembers(boardId)
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Error getting members.')
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="flex flex-col gap-3">
    <div v-if="loading" class="font-black uppercase text-sm animate-pulse p-3 bg-yellow-400 border-2 border-black text-center">LOADING...</div>

    <template v-else-if="members.length > 0">
      <div
        v-for="member in members"
        :key="member.user.user_id"
        class="border-4 border-black bg-white p-3 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
      >
        <div class="font-black uppercase text-sm tracking-wide line-clamp-1">{{ member.user.username }}</div>
        <div class="text-xs font-bold uppercase text-indigo-600 mt-1 border-t-2 border-black pt-1">{{ member.role }}</div>
      </div>
    </template>

    <div v-else class="font-black uppercase text-xs text-gray-500 border-2 border-dashed border-gray-400 p-4 text-center">No members</div>
  </div>
</template>
