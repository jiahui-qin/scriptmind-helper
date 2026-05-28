import React, { useEffect, useState, useCallback } from 'react';
import {
  Box, Typography, Paper, CircularProgress, Alert, Button, Stack,
  Chip, LinearProgress, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Grid, IconButton, Tooltip,
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import RefreshIcon from '@mui/icons-material/Refresh';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import { useParams, useNavigate } from 'react-router-dom';
import {
  getAnalysisResult,
  triggerAnalysis,
  triggerTTS,
  type Role,
  type Line,
  type AnalysisResponse,
} from '../services/api';
import RoleCard from '../components/RoleCard';

/** 情感标签对应的 CSS 类名 */
function getEmotionClass(tag: string | null): string {
  if (!tag) return 'emotion-tag emotion-neutral';
  const map: Record<string, string> = {
    '开心': 'emotion-tag emotion-happy',
    'happy': 'emotion-tag emotion-happy',
    '悲伤': 'emotion-tag emotion-sad',
    'sad': 'emotion-tag emotion-sad',
    '愤怒': 'emotion-tag emotion-angry',
    'angry': 'emotion-tag emotion-angry',
    '惊讶': 'emotion-tag emotion-surprised',
    'surprised': 'emotion-tag emotion-surprised',
    '恐惧': 'emotion-tag emotion-fear',
    'fear': 'emotion-tag emotion-fear',
    '中性': 'emotion-tag emotion-neutral',
    'neutral': 'emotion-tag emotion-neutral',
  };
  return map[tag.toLowerCase()] || 'emotion-tag emotion-neutral';
}

/** 情感强度可视化条 */
function EmotionIntensity({ intensity }: { intensity: number | null }) {
  if (intensity === null || intensity === undefined) return null;
  const pct = Math.min(Math.max(intensity * 100, 0), 100);
  return (
    <Box sx={{ display: 'inline-flex', alignItems: 'center', gap: 0.5, ml: 1 }}>
      <Box
        sx={{
          width: 40,
          height: 4,
          borderRadius: 2,
          bgcolor: '#e2e8f0',
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            width: `${pct}%`,
            height: '100%',
            borderRadius: 2,
            bgcolor: pct > 70 ? '#ef4444' : pct > 40 ? '#f59e0b' : '#22c55e',
            transition: 'width 0.3s ease',
          }}
        />
      </Box>
      <Typography variant="caption" color="text.disabled">
        {(intensity * 100).toFixed(0)}%
      </Typography>
    </Box>
  );
}

export default function AnalysisPage() {
  const { scriptId } = useParams<{ scriptId: string }>();
  const navigate = useNavigate();

  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [pollingInterval, setPollingInterval] = useState<ReturnType<typeof setInterval> | null>(null);
  const [roleVoiceMap, setRoleVoiceMap] = useState<Record<number, string>>({});
  const [ttsTriggering, setTtsTriggering] = useState(false);

  // 获取分析结果
  const fetchResult = useCallback(async () => {
    if (!scriptId) return;
    try {
      const res = await getAnalysisResult(Number(scriptId));
      const data = res.data;
      setAnalysisData(data);

      // 如果已分析完成，停止轮询
      if (data.is_analyzed) {
        if (pollingInterval) {
          clearInterval(pollingInterval);
          setPollingInterval(null);
        }
        setAnalyzing(false);
      }
    } catch (e: any) {
      if (e.response?.status === 404) {
        setError('分析尚未完成，请先触发分析。');
      } else {
        setError(e.response?.data?.detail || e.message || '获取分析结果失败');
      }
    } finally {
      setLoading(false);
    }
  }, [scriptId, pollingInterval]);

  useEffect(() => {
    fetchResult();
    return () => {
      if (pollingInterval) clearInterval(pollingInterval);
    };
  }, [scriptId]);

  // 触发分析
  const handleTrigger = async () => {
    if (!scriptId) return;
    setAnalyzing(true);
    setError('');
    try {
      await triggerAnalysis(Number(scriptId));
      // 开始轮询
      const interval = setInterval(fetchResult, 3000);
      setPollingInterval(interval);
    } catch (e: any) {
      setError(e.response?.data?.detail || e.message || '触发分析失败');
      setAnalyzing(false);
    }
  };

  // 停止轮询
  const stopPolling = () => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
    }
    setAnalyzing(false);
  };

  // 手动刷新
  const handleRefresh = () => {
    setLoading(true);
    setError('');
    fetchResult();
  };

  // 更新角色音色映射
  const handleVoiceChange = (roleId: number, voiceType: string) => {
    setRoleVoiceMap((prev) => ({ ...prev, [roleId]: voiceType }));
  };

  // 更新角色字段
  const handleRoleUpdate = (roleId: number, field: string, value: string) => {
    setAnalysisData((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        roles: prev.roles.map((r) =>
          r.id === roleId ? { ...r, [field]: value } : r
        ),
      };
    });
  };

  // 触发 TTS 合成
  const handleTriggerTTS = async () => {
    if (!scriptId) return;
    setTtsTriggering(true);
    try {
      const res = await triggerTTS(Number(scriptId));
      const taskId = res.data.task_id;
      navigate(`/result/${taskId}`);
    } catch (e: any) {
      setError(e.response?.data?.detail || e.message || 'TTS 合成触发失败');
      setTtsTriggering(false);
    }
  };

  // ── 角色名称映射（供台词表格使用） ──
  const roleNameMap: Record<number, string> = {};
  if (analysisData?.roles) {
    analysisData.roles.forEach((r) => {
      roleNameMap[r.id] = r.name;
    });
  }

  // ── 加载中 ──
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress sx={{ color: '#6366f1' }} />
      </Box>
    );
  }

  // ── 未分析状态 ──
  if (!analysisData || (!analysisData.is_analyzed && !analyzing)) {
    return (
      <Box sx={{ maxWidth: 700, mx: 'auto', py: 6 }}>
        <Paper
          elevation={0}
          sx={{
            p: 6,
            textAlign: 'center',
            border: '2px dashed #e2e8f0',
            borderRadius: 3,
          }}
        >
          <AutoFixHighIcon sx={{ fontSize: 56, color: '#6366f1', mb: 2 }} />
          <Typography variant="h5" fontWeight={700} gutterBottom>
            开始 AI 分析
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 4, lineHeight: 1.8 }}>
            AI 将自动分析台本中的角色信息、性格特征，
            <br />
            并为每句台词标注情感标签和强度。
          </Typography>

          {error && (
            <Alert severity="warning" sx={{ mb: 3, textAlign: 'left' }}>
              {error}
            </Alert>
          )}

          <Button
            variant="contained"
            size="large"
            onClick={handleTrigger}
            disabled={analyzing}
            startIcon={analyzing ? <CircularProgress size={20} color="inherit" /> : <AutoFixHighIcon />}
            sx={{
              px: 4,
              py: 1.5,
              fontWeight: 600,
              fontSize: '1rem',
              borderRadius: 2,
              background: 'linear-gradient(135deg, #6366f1, #a855f7)',
              '&:hover': {
                background: 'linear-gradient(135deg, #4f46e5, #9333ea)',
              },
            }}
          >
            {analyzing ? '分析中...' : '触发 AI 分析'}
          </Button>

          <Box sx={{ mt: 2 }}>
            <Button variant="text" startIcon={<ArrowBackIcon />} onClick={() => navigate('/')}>
              返回首页
            </Button>
          </Box>
        </Paper>
      </Box>
    );
  }

  // ── 分析进行中 ──
  if (analyzing && !analysisData?.is_analyzed) {
    return (
      <Box sx={{ maxWidth: 700, mx: 'auto', py: 6, textAlign: 'center' }}>
        <CircularProgress size={60} sx={{ color: '#6366f1', mb: 3 }} />
        <Typography variant="h5" fontWeight={700} gutterBottom>
          AI 正在分析台本...
        </Typography>
        <Typography color="text.secondary" sx={{ mb: 3 }}>
          正在识别角色、分析性格特征、标注情感标签，请稍候
        </Typography>
        <LinearProgress
          sx={{
            height: 6,
            borderRadius: 3,
            maxWidth: 400,
            mx: 'auto',
            '& .MuiLinearProgress-bar': {
              background: 'linear-gradient(90deg, #6366f1, #a855f7, #ec4899)',
              backgroundSize: '200% 100%',
              animation: 'shimmer 2s infinite',
            },
          }}
        />
        <Box sx={{ mt: 3 }}>
          <Button variant="outlined" onClick={stopPolling} size="small">
            停止等待
          </Button>
        </Box>
      </Box>
    );
  }

  // ── 分析完成 ──
  const roles = analysisData.roles || [];
  const lines = analysisData.lines || [];

  return (
    <Box sx={{ py: 2 }}>
      {/* ── 顶部操作栏 ──────────────────────── */}
      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        justifyContent="space-between"
        alignItems={{ xs: 'stretch', sm: 'center' }}
        mb={4}
        gap={2}
      >
        <Box>
          <Typography variant="h5" fontWeight={700}>
            分析结果
          </Typography>
          <Typography variant="body2" color="text.secondary">
            脚本 ID: {scriptId} · {roles.length} 个角色 · {lines.length} 句台词
          </Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Tooltip title="重新分析">
            <IconButton onClick={handleTrigger} disabled={analyzing} sx={{ border: '1px solid #e2e8f0' }}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Button
            variant="contained"
            startIcon={<PlayArrowIcon />}
            onClick={handleTriggerTTS}
            disabled={ttsTriggering || roles.length === 0}
            sx={{
              fontWeight: 600,
              borderRadius: 2,
              background: 'linear-gradient(135deg, #6366f1, #a855f7)',
              '&:hover': { background: 'linear-gradient(135deg, #4f46e5, #9333ea)' },
            }}
          >
            {ttsTriggering ? '生成中...' : '生成语音'}
          </Button>
        </Stack>
      </Stack>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* ── 角色卡片区域 ────────────────────── */}
      <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>
        角色列表
      </Typography>
      <Grid container spacing={3} sx={{ mb: 5 }}>
        {roles.map((role) => (
          <Grid size={{ xs: 12, sm: 6, lg: 4 }} key={role.id}>
            <RoleCard
              role={role}
              voiceType={roleVoiceMap[role.id] || role.voice_type || 'default'}
              onVoiceChange={handleVoiceChange}
              onRoleUpdate={handleRoleUpdate}
            />
          </Grid>
        ))}
      </Grid>

      {/* ── 台词表格 ────────────────────────── */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" fontWeight={600}>
          台词列表
        </Typography>
        <Chip label={`共 ${lines.length} 句`} size="small" variant="outlined" />
      </Box>

      <TableContainer
        component={Paper}
        elevation={0}
        sx={{ border: '1px solid #e2e8f0', borderRadius: 3, maxHeight: 500 }}
      >
        <Table stickyHeader size="small">
          <TableHead>
            <TableRow sx={{ bgcolor: '#f8fafc' }}>
              <TableCell sx={{ fontWeight: 600, width: 60 }}>序号</TableCell>
              <TableCell sx={{ fontWeight: 600, width: 100 }}>角色</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>台词内容</TableCell>
              <TableCell sx={{ fontWeight: 600, width: 140 }}>情感标签</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {lines.map((line) => (
              <TableRow
                key={line.id}
                sx={{
                  '&:hover': { bgcolor: '#f8fafc' },
                  bgcolor: line.role_id ? 'transparent' : '#fffbeb',
                }}
              >
                <TableCell sx={{ color: '#94a3b8', fontVariantNumeric: 'tabular-nums' }}>
                  #{line.line_number}
                </TableCell>
                <TableCell>
                  {line.role_id ? (
                    <Chip
                      label={roleNameMap[line.role_id] || `角色${line.role_id}`}
                      size="small"
                      sx={{
                        bgcolor: '#eef2ff',
                        color: '#6366f1',
                        fontWeight: 500,
                        fontSize: '0.75rem',
                      }}
                    />
                  ) : (
                    <Chip
                      label="旁白"
                      size="small"
                      variant="outlined"
                      sx={{ fontSize: '0.75rem', borderColor: '#fde68a', color: '#92400e' }}
                    />
                  )}
                </TableCell>
                <TableCell>
                  <Typography variant="body2" sx={{ lineHeight: 1.6 }}>
                    {line.content}
                  </Typography>
                </TableCell>
                <TableCell>
                  {line.emotion_tag ? (
                    <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 0.5 }}>
                      <span className={getEmotionClass(line.emotion_tag)}>
                        {line.emotion_tag}
                      </span>
                      <EmotionIntensity intensity={line.emotion_intensity} />
                    </Box>
                  ) : (
                    <Typography variant="caption" color="text.disabled">
                      -
                    </Typography>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* ── 底部导航 ─────────────────────────── */}
      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <Button variant="text" startIcon={<ArrowBackIcon />} onClick={() => navigate('/')}>
          返回首页
        </Button>
      </Box>
    </Box>
  );
}
