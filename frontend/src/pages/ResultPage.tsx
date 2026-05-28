import React, { useEffect, useState, useCallback, useRef } from 'react';
import {
  Box, Typography, Button, Container, Alert, CircularProgress,
  Stack, Paper, Chip, LinearProgress,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';
import PendingIcon from '@mui/icons-material/Pending';
import { getTTSResult, type TTSStatusResponse } from '../services/api';
import AudioPlayer from '../components/AudioPlayer';

/** 状态对应的显示信息 */
const STATUS_CONFIG: Record<
  string,
  { label: string; icon: React.ReactNode; color: 'default' | 'primary' | 'success' | 'warning' | 'error' }
> = {
  pending: {
    label: '等待处理',
    icon: <PendingIcon />,
    color: 'default',
  },
  processing: {
    label: '合成中',
    icon: <HourglassEmptyIcon />,
    color: 'primary',
  },
  completed: {
    label: '已完成',
    icon: <CheckCircleIcon />,
    color: 'success',
  },
  failed: {
    label: '失败',
    icon: <ErrorIcon />,
    color: 'error',
  },
};

export default function ResultPage() {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();

  const [status, setStatus] = useState<TTSStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // 获取 TTS 任务状态
  const fetchStatus = useCallback(async () => {
    if (!taskId) return;
    try {
      const res = await getTTSResult(taskId);
      setStatus(res.data);

      // 如果任务已结束（完成或失败），停止轮询
      if (res.data.status === 'completed' || res.data.status === 'failed') {
        if (pollingRef.current) {
          clearInterval(pollingRef.current);
          pollingRef.current = null;
        }
      }
    } catch (e: any) {
      setError(e.response?.data?.detail || e.message || '获取任务状态失败');
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
        pollingRef.current = null;
      }
    } finally {
      setLoading(false);
    }
  }, [taskId]);

  useEffect(() => {
    fetchStatus();

    // 开始轮询（每 3 秒检查一次）
    pollingRef.current = setInterval(fetchStatus, 3000);

    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
    };
  }, [fetchStatus]);

  // 手动刷新
  const handleRefresh = () => {
    setLoading(true);
    setError('');
    fetchStatus();
  };

  // ── 加载中 ──
  if (loading) {
    return (
      <Container maxWidth="md">
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
          <CircularProgress sx={{ color: '#6366f1' }} />
        </Box>
      </Container>
    );
  }

  // ── 错误 ──
  if (error && !status) {
    return (
      <Container maxWidth="md">
        <Box sx={{ py: 6, textAlign: 'center' }}>
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
          <Stack direction="row" spacing={2} justifyContent="center">
            <Button variant="outlined" onClick={handleRefresh}>
              重试
            </Button>
            <Button variant="text" startIcon={<ArrowBackIcon />} onClick={() => navigate('/')}>
              返回首页
            </Button>
          </Stack>
        </Box>
      </Container>
    );
  }

  if (!status) return null;

  const statusConfig = STATUS_CONFIG[status.status] || STATUS_CONFIG.pending;

  return (
    <Container maxWidth="md">
      <Box sx={{ py: 4 }}>
        {/* ── 标题栏 ──────────────────────────── */}
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          justifyContent="space-between"
          alignItems={{ xs: 'stretch', sm: 'center' }}
          mb={4}
          gap={2}
        >
          <Box>
            <Typography variant="h5" fontWeight={700} gutterBottom>
              TTS 合成结果
            </Typography>
            <Typography variant="body2" color="text.secondary">
              任务 ID: {taskId}
            </Typography>
          </Box>
          <Button
            variant="text"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/')}
          >
            返回首页
          </Button>
        </Stack>

        {/* ── 状态卡片 ────────────────────────── */}
        <Paper
          elevation={0}
          sx={{
            p: 3,
            mb: 4,
            border: '1px solid #e2e8f0',
            borderRadius: 3,
          }}
        >
          <Typography variant="subtitle1" fontWeight={600} gutterBottom>
            任务状态
          </Typography>

          <Stack direction="row" spacing={1.5} alignItems="center" mb={2}>
            <Chip
              icon={statusConfig.icon as React.ReactElement}
              label={statusConfig.label}
              color={statusConfig.color}
              variant={statusConfig.color === 'default' ? 'outlined' : 'filled'}
              size="small"
            />
            {status.status === 'processing' && (
              <Typography variant="caption" color="text.secondary">
                进度: {status.progress || 0}%
              </Typography>
            )}
          </Stack>

          {/* 处理中的进度条 */}
          {status.status === 'processing' && (
            <LinearProgress
              variant="determinate"
              value={status.progress || 0}
              sx={{
                height: 6,
                borderRadius: 3,
                mb: 2,
                bgcolor: '#e2e8f0',
                '& .MuiLinearProgress-bar': {
                  borderRadius: 3,
                  background: 'linear-gradient(90deg, #6366f1, #a855f7)',
                },
              }}
            />
          )}

          {status.status === 'pending' && (
            <Alert severity="info" sx={{ borderRadius: 2 }}>
              任务已加入队列，正在等待处理...
            </Alert>
          )}

          {status.status === 'failed' && (
            <Alert severity="error" sx={{ borderRadius: 2 }}>
              合成失败: {status.error_message || '未知错误'}
            </Alert>
          )}
        </Paper>

        {/* ── 音频播放器 ──────────────────────── */}
        {status.status === 'completed' && status.audio_url && (
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>
              音频播放
            </Typography>
            <AudioPlayer
              audioUrl={status.audio_url}
              srtUrl={status.subtitle_url || undefined}
              title={`台本语音合成 - ${taskId}`}
            />
          </Box>
        )}

        {/* ── 下载区域（完成但未集成播放器时） ── */}
        {status.status === 'completed' && !status.audio_url && (
          <Alert severity="warning" sx={{ borderRadius: 2 }}>
            任务已完成，但音频文件暂不可用。请稍后刷新页面。
          </Alert>
        )}

        {/* ── 底部操作 ────────────────────────── */}
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Button variant="outlined" onClick={handleRefresh} sx={{ mr: 2 }}>
            刷新状态
          </Button>
          <Button variant="text" startIcon={<ArrowBackIcon />} onClick={() => navigate('/')}>
            返回首页
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
