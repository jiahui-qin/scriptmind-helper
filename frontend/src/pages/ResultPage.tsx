import React from 'react'
import { Box, Typography, Button, Container } from '@mui/material'
import { useParams, useNavigate } from 'react-router-dom'

export default function ResultPage() {
  const { taskId } = useParams<{ taskId: string }>()
  const navigate = useNavigate()

  return (
    <Container maxWidth="md">
      <Box sx={{ py: 4 }}>
        <Typography variant="h5" gutterBottom>合成结果</Typography>
        <Typography>任务 ID: {taskId}</Typography>
        <Typography sx={{ mt: 2, color: 'text.secondary' }}>
          音频和字幕文件生成后，将在此处显示下载链接。
        </Typography>
        <Button sx={{ mt: 2 }} onClick={() => navigate('/')}>返回首页</Button>
      </Box>
    </Container>
  )
}
