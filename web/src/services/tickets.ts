import { api } from '@/services/api'
import type { SimpleTicketResponse } from '@/types/ticket'

export async function getBoardTickets(board_id: number): Promise<SimpleTicketResponse[]> {
  const { data } = await api.get<SimpleTicketResponse[]>(`/tickets/board/${board_id}`)
  return data
}
