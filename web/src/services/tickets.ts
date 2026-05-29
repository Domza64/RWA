import { api } from '@/services/api'
import type { SimpleTicket } from '@/types/ticket'

export async function getBoardTickets(board_id: number): Promise<SimpleTicket[]> {
  const { data } = await api.get<SimpleTicket[]>(`/tickets/board/${board_id}`)
  return data
}

export async function createTicket(
  board_id: number,
  title: string,
  description: string,
  urgency: number,
  due_date?: string | null,
  asignee_id?: number | null,
  current_stage?: number | null,
): Promise<void> {
  await api.post<void>(`/boards/${board_id}/ticket`, {
    title,
    description,
    due_date,
    urgency,
    asignee_id,
    current_stage,
  })
}
