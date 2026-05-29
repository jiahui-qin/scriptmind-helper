import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Types ──────────────────────────────────────────────────────

export interface ScriptUploadResponse {
  id: number;
  filename: string;
  file_size: number;
  status: string;
  created_at: string;
}

export interface Role {
  id: number;
  script_id?: number;
  name: string;
  gender: string;
  age_range?: string;
  age?: number;
  voice_type?: string;
  personality: string;
  description: string;
  line_count?: number;
  tone_style?: string;
  voice_color?: string;
  persona_accent?: string;
  dialect?: string;
  roleplay?: string;
  singing?: string;
}

export interface Line {
  id: number;
  script_id?: number;
  role_id: number | null;
  line_number: number;
  content: string;
  emotion_tag: string | null;
  emotion_intensity: number | null;
  complex_emotion?: string;
  order_index?: number;
}

export interface AnalysisResponse {
  script_id: number;
  is_analyzed: boolean;
  roles_count: number;
  lines_count: number;
  roles: Role[];
  lines: Line[];
}

export interface TTSStatusResponse {
  task_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  audio_url: string | null;
  subtitle_url: string | null;
  error_message: string | null;
}

export interface TTSVoice {
  id: string;
  name: string;
  gender: string;
  description: string;
}

export interface ConfigStatus {
  moonshot_api_configured: boolean;
  database_type: string;
  redis_configured: boolean;
  max_file_size_mb: number;
  features: {
    upload: boolean;
    analysis: boolean;
    tts: boolean;
  };
}

// ── Upload ─────────────────────────────────────────────────────

export const uploadScript = (file: File) => {
  const fd = new FormData();
  fd.append('file', file);
  return api.post<ScriptUploadResponse>('/upload/script', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const listScripts = (skip = 0, limit = 100) =>
  api.get<ScriptUploadResponse[]>('/upload/scripts', { params: { skip, limit } });

export const getScript = (scriptId: number) =>
  api.get<ScriptUploadResponse>(`/upload/script/${scriptId}`);

// ── Analysis ───────────────────────────────────────────────────

export const triggerAnalysis = (scriptId: number) =>
  api.post<{ script_id: number; status: string; message: string }>(
    `/analysis/${scriptId}/analyze`
  );

export const getAnalysisResult = (scriptId: number) =>
  api.get<AnalysisResponse>(`/analysis/${scriptId}`);

// ── TTS ────────────────────────────────────────────────────────

export const triggerTTS = (scriptId: number, roleVoiceMap?: Record<number, string>, includeNarration = true, narrationVoice = "冰糖", lineGapMs = 0) =>
  api.post<{ script_id: number; task_id: number; status: string }>(
    `/tts/${scriptId}/synthesize`,
    { role_voice_map: roleVoiceMap || {}, include_narration: includeNarration, narration_voice: narrationVoice, line_gap_ms: lineGapMs }
  );

export const getTTSResult = (taskId: string) =>
  api.get<TTSStatusResponse>(`/tts/tasks/${taskId}`);

export const listTTSTasks = (scriptId?: number) =>
  api.get<TTSStatusResponse[]>('/tts/tasks', { params: { script_id: scriptId } });

export const getTTSVoices = () =>
  api.get<TTSVoice[]>('/tts/voices');

// ── Config ─────────────────────────────────────────────────────

export const getConfigStatus = () =>
  api.get<ConfigStatus>('/config/status');

export const updateConfig = (data: { mimo_api_key: string }) =>
  api.post('/config/', data);

export default api;

export const deleteScript = (scriptId: number) =>
  api.delete(`/upload/script/${scriptId}`);

// --- Roles ---
export const updateRole = (roleId: number, data: Record<string, any>) =>
  api.put(`/roles/${roleId}`, data)

export const getVoices = () => [
  "mimo_default", "冰糖", "茉莉", "苏打", "白桦", "Mia", "Chloe", "Milo", "Dean",
]

// ── Lines ──────────────────────────────────────────────────────

export const updateLine = (lineId: number, data: {
  role_id?: number | null; emotion_tag?: string; complex_emotion?: string; emotion_intensity?: number
}) => api.put(`/lines/${lineId}`, data);

export const batchUpdateLines = (data: {
  mode: 'by_ids' | 'by_role';
  line_ids?: number[];
  script_id?: number;
  from_role_id?: number | null;
  updates: { role_id?: number | null; emotion_tag?: string; complex_emotion?: string }
}) => api.post('/lines/batch', data);

// ── Roles ──────────────────────────────────────────────────────

export const createRole = (scriptId: number, data: {
  name: string; gender?: string; age?: number; personality?: string;
  tone_style?: string; voice_color?: string; persona_accent?: string;
  dialect?: string; roleplay?: string; singing?: string;
}) => api.post(`/scripts/${scriptId}/roles`, data);

// ── Styles ─────────────────────────────────────────────────────

export const getStyles = (category: string) =>
  api.get<{ category: string; builtin: string[]; custom: string[]; all: string[] }>(`/styles/${category}`);

export const addStyle = (category: string, value: string) =>
  api.post(`/styles/?category=${encodeURIComponent(category)}&value=${encodeURIComponent(value)}`);
