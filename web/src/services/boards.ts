import type { Board, Member } from '@/types/board'
import { api } from '@/services/api'
import type { WorkflowStage } from '@/types/ticket'

export async function getBoards(): Promise<Board[]> {
  const { data } = await api.get<Board[]>('/boards')
  return data
}

export async function getBoard(board_id: number): Promise<Board> {
  const { data } = await api.get<Board>(`/boards/${board_id}`)
  return data
}

type CreateBoardResponse = { board_id: number }
export async function createBoard(name: string, description: string): Promise<number> {
  const { data } = await api.post<CreateBoardResponse>('/boards', { name, description })
  return data.board_id
}

export async function getMembers(board_id: number): Promise<Member[]> {
  const { data } = await api.get<Member[]>(`/boards/${board_id}/members`)
  return data
}

export async function getWorkflowStages(board_id: number): Promise<WorkflowStage[]> {
  const { data } = await api.get<WorkflowStage[]>(`/boards/${board_id}/workflow-stages`)
  return data
}
