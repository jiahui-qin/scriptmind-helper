import React from 'react';
import {
  Box, Typography, Button, Container, Paper, Grid,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import PsychologyIcon from '@mui/icons-material/Psychology';
import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAlt';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ScriptUploader from '../components/ScriptUploader';

const features = [
  {
    icon: <PsychologyIcon sx={{ fontSize: 40 }} />,
    title: 'AI 角色分析',
    description: '基于大语言模型智能识别台本中的角色信息，自动分析性格特征、年龄范围和性别属性，省去手动标注的繁琐工作。',
    color: '#6366f1',
    bgColor: '#eef2ff',
  },
  {
    icon: <SentimentSatisfiedAltIcon sx={{ fontSize: 40 }} />,
    title: '情感标注',
    description: '自动为每句台词标注情感标签（开心、悲伤、愤怒、惊讶、恐惧、中性），并评估情感强度，让配音演绎更有层次。',
    color: '#ec4899',
    bgColor: '#fdf2f8',
  },
  {
    icon: <RecordVoiceOverIcon sx={{ fontSize: 40 }} />,
    title: 'TTS 语音合成',
    description: '一键将台本转化为高质量语音，支持多角色音色映射，自动生成 WAV 音频和 SRT 字幕文件，加速配音制作流程。',
    color: '#8b5cf6',
    bgColor: '#f5f3ff',
  },
];

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <Box>
      {/* ── Hero 区域 ──────────────────────────────── */}
      <Box
        sx={{
          textAlign: 'center',
          py: { xs: 6, md: 10 },
          px: 2,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* 背景装饰 */}
        <Box
          sx={{
            position: 'absolute',
            top: -100,
            left: '50%',
            transform: 'translateX(-50%)',
            width: 600,
            height: 600,
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%)',
            pointerEvents: 'none',
          }}
        />

        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Box sx={{ display: 'inline-flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <AutoAwesomeIcon sx={{ color: '#6366f1', fontSize: 20 }} />
            <Typography
              variant="body2"
              sx={{
                color: '#6366f1',
                fontWeight: 600,
                letterSpacing: 1,
                textTransform: 'uppercase',
              }}
            >
              AI-Powered Script Analysis
            </Typography>
          </Box>

          <Typography
            variant="h2"
            fontWeight={800}
            sx={{
              fontSize: { xs: '2rem', md: '3rem' },
              background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 2,
            }}
          >
            ScriptMind AI
          </Typography>

          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ maxWidth: 600, mx: 'auto', mb: 1, fontWeight: 400, lineHeight: 1.8 }}
          >
            台本分析助手 — 上传你的台本文件，AI 自动识别角色、
            分析性格特征、标注情感色彩，并一键生成多角色语音
          </Typography>

          <Typography variant="body2" color="text.disabled" sx={{ mb: 4 }}>
            支持中文剧本、广播剧、有声书等 .txt 格式文本
          </Typography>
        </Box>
      </Box>

      {/* ── 功能特性卡片 ───────────────────────────── */}
      <Container maxWidth="lg" sx={{ mb: 6 }}>
        <Typography
          variant="h5"
          fontWeight={700}
          textAlign="center"
          sx={{ mb: 1 }}
        >
          核心功能
        </Typography>
        <Typography
          variant="body2"
          color="text.secondary"
          textAlign="center"
          sx={{ mb: 4 }}
        >
          一站式解决台本分析到语音合成的全流程
        </Typography>

        <Grid container spacing={3}>
          {features.map((feature, index) => (
            <Grid size={{ xs: 12, md: 4 }} key={index}>
              <Paper
                elevation={0}
                sx={{
                  p: 4,
                  height: '100%',
                  border: '1px solid #e2e8f0',
                  borderRadius: 3,
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    borderColor: feature.color,
                    boxShadow: '0 4px 24px rgba(0,0,0,0.06)',
                    transform: 'translateY(-2px)',
                  },
                }}
              >
                <Box
                  sx={{
                    display: 'inline-flex',
                    p: 1.5,
                    borderRadius: 2,
                    bgcolor: feature.bgColor,
                    color: feature.color,
                    mb: 2,
                  }}
                >
                  {feature.icon}
                </Box>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.8 }}>
                  {feature.description}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* ── 上传区域 ──────────────────────────────── */}
      <Container maxWidth="md" sx={{ mb: 8 }}>
        <ScriptUploader />
        <Box sx={{ textAlign: 'center', mt: 3 }}>
          <Button
            variant="text"
            onClick={() => navigate('/config')}
            sx={{
              color: '#64748b',
              '&:hover': { color: '#6366f1' },
            }}
          >
            需要先配置 API Key？前往设置 →
          </Button>
        </Box>
      </Container>

      {/* ── Footer ────────────────────────────────── */}
      <Box sx={{ textAlign: 'center', py: 3, borderTop: '1px solid #e2e8f0' }}>
        <Typography variant="caption" color="text.disabled">
          ScriptMind AI · 台本分析助手 · Powered by Moonshot AI &amp; MiMo TTS
        </Typography>
      </Box>
    </Box>
  );
}
