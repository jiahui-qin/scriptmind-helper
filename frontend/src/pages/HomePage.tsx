import React from 'react';
import { Box, Typography, Container, Grid, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAlt';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import ScriptUploader from '../components/ScriptUploader';

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

export default function HomePage() {
  const navigate = useNavigate();

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
