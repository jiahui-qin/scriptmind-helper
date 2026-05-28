export interface Role {
  id: number
  script_id: number
  name: string
  gender: string
  age: number
  voice_type: string
  personality: string
  description: string
}

export interface Line {
  id: number
  script_id: number
  role_id: number | null
  line_number: number
  content: string
  emotion_tag: string | null
  emotion_intensity: number | null
}

export interface ScriptUploadResponse {
  id: number
  filename: string
  file_size: number
  created_at: string
}
