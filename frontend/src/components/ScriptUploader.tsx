import React, { useState } from 'react'
import {
  Box, Button, Typography, Paper, LinearProgress, Alert, Stack,
} from '@mui/material'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import { useMutation } from '@tanstack/react-query'
import { uploadScript, type ScriptUploadResponse } from '../services/api'
import { useStore } from '../store/useStore'

export default function ScriptUploader() {
  const [file, setFile] = useState<File | null>(null)
  const setScriptId = useStore(s => s.setScriptId)

  const mutation = useMutation({
    mutationFn: (f: File) => uploadScript(f).then(r => r.data),
    onSuccess: (data: ScriptUploadResponse) => {
      setScriptId(data.id)
    },
  })

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setFile(e.target.files[0])
  }

  const handleUpload = () => {
    if (file) mutation.mutate(file)
  }

  return (
    <Paper sx={{ p: 4, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        上传台本文件
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 2 }}>
        支持 .txt 格式，单个文件不超过 10MB
      </Typography>

      <Stack direction="row" spacing={2} alignItems="center">
        <Button
          variant="outlined"
          component="label"
          startIcon={<CloudUploadIcon />}
        >
          {file ? file.name : '选择文件'}
          <input type="file" accept=".txt" hidden onChange={handleFileChange} />
        </Button>
        <Button
          variant="contained"
          disabled={!file || mutation.isPending}
          onClick={handleUpload}
        >
          上传
        </Button>
      </Stack>

      {mutation.isPending && <LinearProgress sx={{ mt: 2 }} />}
      {mutation.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {(mutation.error as Error).message}
        </Alert>
      )}
      {mutation.isSuccess && (
        <Alert severity="success" sx={{ mt: 2 }}>
          上传成功！Script ID: {mutation.data.id}
        </Alert>
      )}
    </Paper>
  )
}
