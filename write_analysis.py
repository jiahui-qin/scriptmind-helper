code = """import React, { useEffect, useState, useCallback, useRef } from 'react';
import {
  Box, Typography, Paper, LinearProgress, Alert, Button, Chip, Stack, Grid,
} from '@mui/material';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useParams, useNavigate } from 'react-router-dom';
import { getAnalysisResult, triggerAnalysis, type Role, type Line } from '../services/api';
import RoleCard from '../components/RoleCard';

const STATUS_LABELS: Record<string, string> = {
  uploaded: '等待分析',
  queued: '已加入队列',
  parsing: '正在解析台本...',
  analyzing_roles: 'MiMo AI 正在分析角色性格...',
  tagging_emotions: 'MiMo AI 正在标注情感...',
  completed: '分析完成',
  failed: '分析失败',
};

function getStatusIcon(status: string) {
  if (status === 'completed') return String.fromCodePoint(0x2705);
  if (status === 'failed') return String.fromCodePoint(0x274C);
  return String.fromCodePoint(0x1F504);
}

export default function AnalysisPage() {
  const { scriptId } = useParams<{ scriptId: string }>();
  const navigate = useNavigate();
  const [roles, setRoles] = useState<Role[]>([]);
  const [lines, setLines] = useState<Line[]>([]);
  const [status, setStatus] = useState('uploaded');
  const [progress, setProgress] = useState(0);
  const [errorMsg, setErrorMsg] = useState('');
  const [isPolling, setIsPolling] = useState(false);
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchResult = useCallback(async () => {
    if (!scriptId) return;
    try {
      const res = await getAnalysisResult(Number(scriptId));
      const data = res.data as any;
      setStatus(data.status || 'uploaded');
      setProgress(data.progress || 0);
      setErrorMsg(data.error_message || '');
      if (data.roles?.length > 0) setRoles(data.roles);
      if (data.lines?.length > 0) setLines(data.lines);
      return data.status;
    } catch (e: any) {
      setErrorMsg(e.message);
      return 'error';
    }
  }, [scriptId]);

  useEffect(() => { fetchResult(); }, [fetchResult]);

  const startPolling = useCallback(() => {
    if (pollingRef.current) return;
    setIsPolling(true);
    pollingRef.current = setInterval(async () => {
      const s = await fetchResult();
      if (s === 'completed' || s === 'failed' || s === 'error') {
        if (pollingRef.current) clearInterval(pollingRef.current);
        pollingRef.current = null;
        setIsPolling(false);
      }
    }, 2000);
  }, [fetchResult]);

  useEffect(() => {
    return () => { if (pollingRef.current) clearInterval(pollingRef.current); };
  }, []);

  const handleTrigger = async () => {
    if (!scriptId) return;
    try {
      setErrorMsg('');
      await triggerAnalysis(Number(scriptId));
      setStatus('queued');
      startPolling();
    } catch (e: any) {
      setErrorMsg(e.message);
    }
  };

  const isRunning = status !== 'completed' && status !== 'failed';

  return (
    <Box sx={{ p: { xs: 2, md: 4 }, maxWidth: 1000, mx: 'auto' }}>
      <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 3 }}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')} size="small">返回</Button>
        <Typography variant="h5" fontWeight={700}>台本分析</Typography>
      </Stack>
      {(isRunning || status === 'completed') && (
        <Paper sx={{ p: 3, mb: 3, border: '1px solid #e2e8f0', borderRadius: 3 }}>
          <Stack spacing={2}>
            <Stack direction="row" alignItems="center" spacing={1}>
              <Typography variant="h6">{getStatusIcon(status)} {STATUS_LABELS[status] || status}</Typography>
            </Stack>
            {isRunning && <>
              <LinearProgress variant={progress > 0 ? 'determinate' : 'indeterminate'} value={progress} sx={{ height: 8, borderRadius: 4 }} />
              <Typography variant="body2" color="text.secondary">{progress > 0 ? progress + '%' : '正在连接 MiMo API...'}</Typography>
            </>}
            {status === 'failed' && <Alert severity="error">{errorMsg ? errorMsg.substring(0, 200) : '分析失败'}</Alert>}
          </Stack>
        </Paper>
      )}
      {status === 'uploaded' && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>台本已上传，点击下方按钮开始 AI 分析</Typography>
          <Button variant="contained" size="large" onClick={handleTrigger} disabled={isPolling}
            startIcon={<AutoFixHighIcon />} sx={{ px: 4, py: 1.5, borderRadius: 2 }}>
            {isPolling ? '分析中...' : '开始分析'}
          </Button>
        </Box>
      )}
      {roles.length > 0 && (
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>识别角色 ({roles.length})</Typography>
          <Grid container spacing={2}>
            {roles.map(r => (
              <Grid item xs={12} sm={6} md={4} key={r.id}>
                <RoleCard role={r} onUpdate={() => {}} />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
      {lines.length > 0 && (
        <Box>
          <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>台词列表 ({lines.length} 行)</Typography>
          <Stack spacing={0.5}>
            {lines.map(line => {
              const role = roles.find(r => r.id === line.role_id);
              return (
                <Paper key={line.id} sx={{ p: 1.5, bgcolor: line.role_id ? '#f8fafc' : '#fffbeb', border: '1px solid #e2e8f0', borderRadius: 2 }}>
                  <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 0.5 }}>
                    <Chip label={role?.name || '旁白'} size="small" color={role ? 'primary' : 'default'} variant="outlined" />
                    <Typography variant="caption" color="text.secondary">#{line.line_number}</Typography>
                    {line.emotion_tag && <span className={'emotion-tag emotion-' + line.emotion_tag}>{line.emotion_tag}</span>}
                  </Stack>
                  <Typography variant="body2">{line.content}</Typography>
                </Paper>
              );
            })}
          </Stack>
        </Box>
      )}
    </Box>
  );
}
"""

with open('/c/Users/pcl/AppData/Local/Temp/scriptmind-helper/frontend/src/pages/AnalysisPage.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
print('OK:', len(code), 'chars')
