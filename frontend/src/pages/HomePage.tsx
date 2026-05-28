import React, { useEffect, useState } from 'react';
import {
  Box, Typography, Container, Grid, Paper, Button, Stack, Chip,
  CircularProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAlt';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import DescriptionIcon from '@mui/icons-material/Description';
import ScriptUploader from '../components/ScriptUploader';
import { listScripts, type ScriptUploadResponse } from '../services/api';

const features = [
  {
    icon: <AutoAwesomeIcon sx={{ fontSize: 40, color: '#6366f1' }} />,
    title: 'AI 角色分析',
    desc: '上传台本，MiMo 大模型自动识别角色，分析性格特征、推荐音色',
  },
  {
    icon: <SentimentSatisfiedAltIcon sx={{ fontSize: 40, color: '#ec4899' }} />,
    title: '情感标注',
    desc: '为每一句台词标注情感标签（开心/悲伤/愤怒等）和情绪强度',
  },
  {
    icon: <RecordVoiceOverIcon sx={{ fontSize: 40, color: '#8b5cf6' }} />,
    title: 'TTS 语音合成',
    desc: 'MiMo TTS 将台词转为自然语音，导出 WAV 音频 + SRT 字幕',
  },
];

/** 状态标签配置 */
const STATUS_CONFIG: Record<string, { label: string; color: 'default' | 'primary' | 'success' | 'warning' | 'error' }> = {
  uploaded: { label: '已上传', color: 'default' },
  queued: { label: '排队中', color: 'primary' },
  parsing: { label: '分析中', color: 'primary' },
  analyzing_roles: { label: '分析中', color: 'primary' },
  tagging_emotions: { label: '分析中', color: 'primary' },
  completed: { label: '已完成', color: 'success' },
  failed: { label: '失败', color: 'error' },
};

export default function HomePage() {
  const navigate = useNavigate();
  const [recentScripts, setRecentScripts] = useState<ScriptUploadResponse[]>([]);
  const [loadingRecent, setLoadingRecent] = useState(true);

  // Load recent 3 scripts
  useEffect(() => {
    let cancelled = false;
    const fetchRecent = async () => {
      try {
        const res = await listScripts(0, 3);
        if (!cancelled) {
          const data: ScriptUploadResponse[] = Array.isArray(res.data) ? res.data : [];
          data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
          setRecentScripts(data.slice(0, 3));
        }
      } catch {
        if (!cancelled) setRecentScripts([]);
      } finally {
        if (!cancelled) setLoadingRecent(false);
      }
    };
    fetchRecent();
    return () => { cancelled = true; };
  }, []);

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          textAlign: 'center',
          py: { xs: 6, md: 10 },
          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
          borderRadius: { xs: 0, md: 4 },
          mx: { xs: -3, md: 0 },
          px: 3,
          mb: 6,
          color: 'white',
        }}
      >
        <Typography
          variant="h2"
          fontWeight={800}
          sx={{ fontSize: { xs: '2rem', md: '3.5rem' }, mb: 2 }}
        >
          ScriptMind AI
        </Typography>
        <Typography
          variant="h6"
          sx={{ opacity: 0.9, mb: 0, maxWidth: 600, mx: 'auto', fontWeight: 400 }}
        >
          台本分析助手 — 上传台本，AI 分析角色性格并生成语音
        </Typography>
      </Box>

      {/* Feature Cards */}
      <Container maxWidth="md">
        <Grid container spacing={3} sx={{ mb: 6 }}>
          {features.map((f, i) => (
            <Grid item xs={12} sm={4} key={i}>
              <Paper
                elevation={0}
                sx={{
                  p: 3,
                  textAlign: 'center',
                  height: '100%',
                  border: '1px solid #e2e8f0',
                  borderRadius: 3,
                  transition: 'box-shadow 0.2s',
                  '&:hover': { boxShadow: '0 4px 20px rgba(0,0,0,0.08)' },
                }}
              >
                <Box sx={{ mb: 1.5 }}>{f.icon}</Box>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  {f.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {f.desc}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>

        {/* ── My Scripts Entry Card ──────────────────── */}
        <Paper
          elevation={0}
          sx={{
            p: 4, mb: 4,
            border: '1px solid #e2e8f0', borderRadius: 3,
            transition: 'box-shadow 0.2s',
            '&:hover': { boxShadow: '0 4px 20px rgba(0,0,0,0.08)' },
          }}
        >
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            justifyContent="space-between"
            alignItems={{ xs: 'stretch', sm: 'center' }}
            spacing={2}
          >
            <Stack direction="row" spacing={2} alignItems="center">
              <Box
                sx={{
                  width: 48, height: 48, borderRadius: 2,
                  bgcolor: '#eef2ff', display: 'flex',
                  alignItems: 'center', justifyContent: 'center',
                }}
              >
                <FolderOpenIcon sx={{ color: '#6366f1' }} />
              </Box>
              <Box>
                <Typography variant="h6" fontWeight={600}>
                  我的台本
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  管理已上传的台本文件，查看分析结果和生成语音
                </Typography>
              </Box>
            </Stack>
            <Button
              variant="outlined"
              onClick={() => navigate('/my-scripts')}
              sx={{
                borderRadius: 2,
                borderColor: '#6366f1',
                color: '#6366f1',
                whiteSpace: 'nowrap',
                '&:hover': { borderColor: '#4f46e5', bgcolor: '#eef2ff' },
              }}
            >
              查看全部
            </Button>
          </Stack>

          {/* ── Recent Scripts Quick Access ──────────── */}
          {loadingRecent && (
            <Box sx={{ textAlign: 'center', py: 2, mt: 2 }}>
              <CircularProgress size={24} sx={{ color: '#6366f1' }} />
            </Box>
          )}

          {!loadingRecent && recentScripts.length > 0 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1.5 }}>
                最近上传
              </Typography>
              <Stack spacing={1}>
                {recentScripts.map((script) => {
                  const statusConfig = STATUS_CONFIG[script.status] || STATUS_CONFIG.uploaded;
                  return (
                    <Paper
                      key={script.id}
                      elevation={0}
                      onClick={() => navigate(`/analysis/${script.id}`)}
                      sx={{
                        p: 1.5, cursor: 'pointer',
                        border: '1px solid #f1f5f9', borderRadius: 2,
                        transition: 'all 0.15s',
                        '&:hover': { borderColor: '#c7d2fe', bgcolor: '#fafafe' },
                      }}
                    >
                      <Stack direction="row" alignItems="center" justifyContent="space-between">
                        <Stack direction="row" spacing={1.5} alignItems="center">
                          <DescriptionIcon sx={{ color: '#94a3b8', fontSize: 20 }} />
                          <Typography variant="body2" fontWeight={500}>
                            {script.filename}
                          </Typography>
                        </Stack>
                        <Chip
                          label={statusConfig.label}
                          color={statusConfig.color}
                          size="small"
                          variant="outlined"
                        />
                      </Stack>
                    </Paper>
                  );
                })}
              </Stack>
            </Box>
          )}

          {!loadingRecent && recentScripts.length === 0 && (
            <Box sx={{ mt: 3, py: 2 }}>
              <Typography variant="body2" color="text.disabled">
                还没有上传台本，上传后即可在此快速访问。
              </Typography>
            </Box>
          )}
        </Paper>
      </Container>

      {/* Upload Area */}
      <Container maxWidth="md">
        <ScriptUploader />
        <Box sx={{ textAlign: 'center', mt: 3 }}>
          <Button variant="text" onClick={() => navigate('/config')}>
            配置 API Key
          </Button>
        </Box>
      </Container>
    </Box>
  );
}
