import React, { useEffect, useState } from 'react'
import {
  Box, Typography, Paper, CircularProgress, Alert, Button, Stack, Chip,
} from '@mui/material'
import { useParams, useNavigate } from 'react-router-dom'
import { getAnalysisResult, triggerAnalysis, type Role, type Line } from '../services/api'

export default function AnalysisPage() {
  const { scriptId } = useParams<{ scriptId: string }>()
  const navigate = useNavigate()
  const [roles, setRoles] = useState<Role[]>([])
  const [lines, setLines] = useState<Line[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [analyzing, setAnalyzing] = useState(false)

  const fetchResult = async () => {
    if (!scriptId) return
    try {
      const res = await getAnalysisResult(Number(scriptId))
      setRoles(res.data.roles)
      setLines(res.data.lines)
    } catch (e: any) {
      if (e.response?.status === 404) {
        setError('分析尚未完成，请先触发分析。')
      } else {
        setError(e.message)
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchResult() }, [scriptId])

  const handleTrigger = async () => {
    if (!scriptId) return
    setAnalyzing(true)
    try {
      await triggerAnalysis(Number(scriptId))
      setTimeout(fetchResult, 3000)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setAnalyzing(false)
    }
  }

  if (loading) return <CircularProgress sx={{ m: 4 }} />
  if (error) return <Alert severity="warning" sx={{ m: 4 }}>{error}</Alert>

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>分析结果</Typography>
      <Button variant="contained" sx={{ mb: 2 }} onClick={handleTrigger} disabled={analyzing}>
        {analyzing ? '分析中...' : '触发分析'}
      </Button>
      <Typography variant="h6" sx={{ mt: 2 }}>角色列表 ({roles.length})</Typography>
      <Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mb: 3 }}>
        {roles.map(r => (
          <Chip key={r.id} label={`${r.name} (${r.gender}, ${r.age}岁)`} color="primary" />
        ))}
      </Stack>
      <Typography variant="h6">台词预览 ({lines.length} 行)</Typography>
      {lines.slice(0, 20).map(line => (
        <Paper key={line.id} sx={{ p: 1, mb: 0.5, bgcolor: line.role_id ? '#f9f9f9' : '#fffde7' }}>
          <Typography variant="caption" color="text.secondary">
            #{line.line_number}
            {line.role_id ? `  [角色${line.role_id}]` : '  [旁白]'}
            {line.emotion_tag ? `  💬${line.emotion_tag}` : ''}
          </Typography>
          <Typography>{line.content}</Typography>
        </Paper>
      ))}
      {lines.length > 20 && (
        <Button onClick={() => navigate(`/result/${scriptId}`)}>查看全部 →</Button>
      )}
    </Box>
  )
}
