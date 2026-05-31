import { api } from '@/services/api'
import type { SimpleTicket, Ticket } from '@/types/ticket'

export async function getBoardTickets(board_id: number): Promise<SimpleTicket[]> {
  const { data } = await api.get<SimpleTicket[]>(`/tickets/board/${board_id}`)
  return data
}

export async function getTicket(ticket_id: number): Promise<Ticket> {
  const { data } = await api.get<Ticket>(`/tickets/${ticket_id}`)
  return data
}

export async function updateTicketStage(ticket_id: number, stage_id: number): Promise<void> {
  await api.patch(`/tickets/${ticket_id}/stage`, { stage_id })
}

export async function updateTicketAssignee(ticket_id: number, user_id: number | null): Promise<void> {
  await api.patch(`/tickets/${ticket_id}/assignee`, { user_id })
}

export async function updateTicketDescription(ticket_id: number, description: string): Promise<void> {
  await api.patch(`/tickets/${ticket_id}`, { description })
}

export async function updateTicketDueDate(ticket_id: number, due_date: string | null): Promise<void> {
  await api.patch(`/tickets/${ticket_id}`, { due_date })
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
