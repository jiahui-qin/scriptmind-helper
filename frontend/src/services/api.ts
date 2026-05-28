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
}

export interface Line {
  id: number;
  script_id?: number;
  role_id: number | null;
  line_number: number;
  content: string;
  emotion_tag: string | null;
  emotion_intensity: number | null;
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

export const updateRole = (roleId: number, data: Partial<Role>) =>
  api.patch<Role>(`/analysis/roles/${roleId}`, data);

// ── TTS ────────────────────────────────────────────────────────

export const triggerTTS = (scriptId: number) =>
  api.post<{ script_id: number; task_id: string; status: string; message: string }>(
    `/tts/${scriptId}/synthesize`
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

export const updateConfig = (data: { moonshot_api_key: string }) =>
  api.post('/config/', data);

export default api;
