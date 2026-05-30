import type { UserData } from './user'

export interface Board {
  board_id: number
  name: string
  description: string
}

export interface Member {
  user: UserData
  role: string
}
