import { ApiError } from '@/services/api'
import type { Board } from '@/types/board'
import { defineStore } from 'pinia'
import { getBoards } from '@/services/boards'
import { ref } from 'vue'

export const useBoardStore = defineStore('boards', () => {
  const boards = ref<Board[]>([])
  const loading = ref(false)
  const loaded = ref(false)

  async function load() {
    if (loading.value || loaded.value) return

    loading.value = true

    try {
      boards.value = await getBoards()
      loaded.value = true
    } catch (e) {
      throw new ApiError('0', 'Error loading boards', 0)
    } finally {
      loading.value = false
    }
  }

  function getBoardsData() {
    if (!loaded.value && !loading.value) {
      load()
    }

    return boards
  }

  return {
    boards: getBoardsData,
    loading,
    loaded,
    load,
  }
})
