import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

export interface ScriptUploadResponse {
  id: number
  filename: string
  file_size: number
  created_at: string
}

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

export const uploadScript = (file: File) => {
  const fd = new FormData()
  fd.append('file', file)
  return api.post<ScriptUploadResponse>('/upload/script', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const triggerAnalysis = (scriptId: number) =>
  api.post(`/analysis/${scriptId}/analyze`)

export const getAnalysisResult = (scriptId: number) =>
  api.get<{ roles: Role[]; lines: Line[] }>(`/analysis/${scriptId}/result`)

export const triggerTTS = (scriptId: number, roleVoiceMap: Record<number, string>) =>
  api.post<{ task_id: number }>('/tts/synthesize', {
    script_id: scriptId,
    role_voice_map: roleVoiceMap,
  })

export const getTTSResult = (taskId: number) =>
  api.get<{ status: string; audio_url: string; srt_url: string }>(`/tts/result/${taskId}`)

export const getConfig = () => api.get<{ mimi_api_key: string }>('/config')
export const updateConfig = (data: { mimi_api_key: string }) =>
  api.post('/config', data)

export default api
