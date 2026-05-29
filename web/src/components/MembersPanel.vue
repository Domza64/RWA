<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getMembers } from '@/services/boards'
import type { Member } from '@/types/board'
import { useNotificationStore } from '@/stores/notification'
import MembersList from './MembersList.vue'

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
  <div class="p-4 h-full border-l border-gray-200">
    <span>Members</span>
    <div v-if="loading">Loading members...</div>
    <div v-else-if="members.length > 0" v-for="member in members" :key="member.user.user_id">
      <div>
        <span class="text-lg">{{ member.user.username }}</span>
        <span class="text-xs text-gray-600">{{ member.role }}</span>
      </div>
    </div>
    <div v-else>No members found.</div>
  </div>
</template>
