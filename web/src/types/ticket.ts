import type { UserData } from './user'

export interface SimpleTicket {
  ticket_id: number
  title: string
  due_date: string
  urgency: number
  assignee: UserData
  current_stage: WorkflowStage | null
}

export interface WorkflowStage {
  workflow_id: number
  stage_id: number
  name: string
}

export interface Ticket {
  ticket_id: number
  title: string
  description: string
  due_date: string
  urgency: number
  assignee: UserData | null
  reporter: UserData | null
  current_stage: WorkflowStage | null
  possible_stages: WorkflowStage[]
}
