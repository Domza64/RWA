import type { Member } from "./board"

export interface Stage {
  stage_id: number
  name: string
}

export interface SimpleTicketResponse {
  ticket_id: number
  title: string
  due_date: string
  urgency: number
  assignee: Member
  current_stage: Stage
}
