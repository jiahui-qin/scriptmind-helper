import React from 'react'
import { Box, Typography, Paper, TextField, Button, Alert, Stack } from '@mui/material'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getConfig, updateConfig } from '../services/api'

export default function ConfigPage() {
  const qc = useQueryClient()
  const { data } = useQuery({ queryKey: ['config'], queryFn: () => getConfig().then(r => r.data) })
  const [key, setKey] = React.useState('')
  React.useEffect(() => { if (data?.moonshot_api_key) setKey(data.moonshot_api_key) }, [data])

  const mutation = useMutation({
    mutationFn: () => updateConfig({ moonshot_api_key: key }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['config'] }),
  })

  return (
    <Box sx={{ p: 4, maxWidth: 600, mx: 'auto' }}>
      <Typography variant="h5" gutterBottom>配置</Typography>
      <Paper sx={{ p: 3 }}>
        <Stack spacing={2}>
          <TextField
            label="MiMo API Key"
            type="password"
            fullWidth
            value={key}
            onChange={e => setKey(e.target.value)}
            helperText="用于角色分析和 TTS 合成，自行提供 MiMo API Key"
          />
          <Button variant="contained" onClick={() => mutation.mutate()} disabled={mutation.isPending}>
            保存配置
          </Button>
          {mutation.isSuccess && <Alert severity="success">保存成功</Alert>}
          {mutation.isError && <Alert severity="error">保存失败</Alert>}
        </Stack>
      </Paper>
    </Box>
  )
}
