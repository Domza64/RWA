import { api } from '@/services/api'
import type { SimpleTicket } from '@/types/ticket'

export async function getBoardTickets(board_id: number): Promise<SimpleTicket[]> {
  const { data } = await api.get<SimpleTicket[]>(`/tickets/board/${board_id}`)
  return data
}
