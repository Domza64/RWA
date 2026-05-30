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
