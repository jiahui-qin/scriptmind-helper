import React from 'react'
import { Box, Typography, Button, Container } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import ScriptUploader from '../components/ScriptUploader'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <Container maxWidth="md">
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h3" fontWeight={700} gutterBottom>
          ScriptMind AI
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 6 }}>
          台本分析助手 — 上传台本，AI 分析角色性格并生成语音
        </Typography>
        <ScriptUploader />
        <Box sx={{ mt: 4 }}>
          <Button variant="text" onClick={() => navigate('/config')}>
            配置 API Key
          </Button>
        </Box>
      </Box>
    </Container>
  )
}
