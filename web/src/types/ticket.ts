import type { Member } from './board'

export interface SimpleTicket {
  ticket_id: number
  title: string
  due_date: string
  urgency: number
  assignee: Member
  current_stage: WorkflowStage
}

export interface WorkflowStage {
  workflow_id: number
  stage_id: number
  name: string
}
