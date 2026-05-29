import type { Board } from '@/types/board'
import { api } from '@/services/api'

export async function getBoards(): Promise<Board[]> {
  const { data } = await api.get<Board[]>('/boards')
  return data
}

type CreateBoardResponse = { board_id: number }
export async function createBoard(name: string, description: string): Promise<number> {
  const { data } = await api.post<CreateBoardResponse>('/boards', { name, description })
  return data.board_id
}
