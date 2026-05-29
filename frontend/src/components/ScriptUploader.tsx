import React, { useState, useRef, useCallback } from 'react';
import {
  Box, Button, Typography, Paper, LinearProgress, Alert, Stack, IconButton,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CloseIcon from '@mui/icons-material/Close';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { uploadScript, triggerAnalysis, type ScriptUploadResponse } from '../services/api';
import { useStore } from '../store/useStore';

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export default function ScriptUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string>('');
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const setScriptId = useStore((s) => s.setScriptId);
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: async (f: File) => {
      const uploadRes = await uploadScript(f);
      const scriptId = uploadRes.data.id;
      // Auto-trigger analysis after upload
      await triggerAnalysis(scriptId);
      return uploadRes.data;
    },
    onSuccess: (data: ScriptUploadResponse) => {
      setScriptId(data.id);
      navigate(`/analysis/${data.id}`);
    },
  });

  const validateFile = (f: File): boolean => {
    if (!f.name.endsWith('.txt')) {
      setFileError('仅支持 .txt 格式的台本文件');
      return false;
    }
    if (f.size > MAX_FILE_SIZE) {
      setFileError(`文件大小超过限制（最大 10MB），当前文件 ${(f.size / 1024 / 1024).toFixed(1)}MB`);
      return false;
    }
    setFileError('');
    return true;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f && validateFile(f)) {
      setFile(f);
    }
  };

  const handleUpload = () => {
    if (file) mutation.mutate(file);
  };

  // 拖拽事件处理
  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    // 只有当离开 drop zone 时才取消高亮
    if (e.currentTarget === e.target || !e.currentTarget.contains(e.relatedTarget as Node)) {
      setIsDragOver(false);
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    const f = e.dataTransfer.files?.[0];
    if (f && validateFile(f)) {
      setFile(f);
    }
  }, []);

  const clearFile = () => {
    setFile(null);
    setFileError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  };

  return (
    <Paper sx={{ p: 4, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Typography variant="h6" fontWeight={600} gutterBottom>
        上传台本文件
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        支持 .txt 格式的剧本文件，单个文件不超过 10MB
      </Typography>

      {/* 拖拽上传区域 */}
      <Box
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        sx={{
          border: '2px dashed',
          borderColor: isDragOver ? 'primary.main' : file ? 'success.main' : '#cbd5e1',
          borderRadius: 3,
          p: 5,
          textAlign: 'center',
          cursor: 'pointer',
          bgcolor: isDragOver ? 'rgba(99, 102, 241, 0.04)' : 'transparent',
          transition: 'all 0.2s ease',
          '&:hover': {
            borderColor: 'primary.main',
            bgcolor: 'rgba(99, 102, 241, 0.04)',
          },
        }}
      >
        {file ? (
          <Stack direction="row" spacing={1} alignItems="center" justifyContent="center">
            <InsertDriveFileIcon sx={{ color: 'primary.main', fontSize: 28 }} />
            <Box sx={{ textAlign: 'left' }}>
              <Typography variant="body1" fontWeight={500} noWrap sx={{ maxWidth: 300 }}>
                {file.name}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {formatFileSize(file.size)}
              </Typography>
            </Box>
            <IconButton
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                clearFile();
              }}
              sx={{ ml: 1 }}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Stack>
        ) : (
          <>
            <CloudUploadIcon sx={{ fontSize: 48, color: '#94a3b8', mb: 1 }} />
            <Typography variant="body1" color="text.secondary">
              拖拽台本文件到此处，或点击选择文件
            </Typography>
            <Typography variant="caption" color="text.disabled">
              仅支持 .txt 格式
            </Typography>
          </>
        )}
        <input
          ref={fileInputRef}
          type="file"
          accept=".txt"
          hidden
          onChange={handleFileChange}
        />
      </Box>

      {/* 文件校验错误 */}
      {fileError && (
        <Alert severity="error" sx={{ mt: 2 }} onClose={() => setFileError('')}>
          {fileError}
        </Alert>
      )}

      {/* 上传按钮 */}
      <Button
        variant="contained"
        fullWidth
        size="large"
        disabled={!file || mutation.isPending}
        onClick={handleUpload}
        sx={{
          mt: 3,
          py: 1.5,
          fontWeight: 600,
          fontSize: '1rem',
          borderRadius: 2,
        }}
      >
        {mutation.isPending ? '上传中...' : '上传并开始分析'}
      </Button>

      {/* 上传进度 */}
      {mutation.isPending && (
        <Box sx={{ mt: 2 }}>
          <LinearProgress
            sx={{
              height: 6,
              borderRadius: 3,
              bgcolor: '#e2e8f0',
              '& .MuiLinearProgress-bar': {
                borderRadius: 3,
                background: 'linear-gradient(90deg, #6366f1, #a855f7, #ec4899)',
                backgroundSize: '200% 100%',
                animation: 'shimmer 2s infinite',
              },
            }}
          />
          <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block', textAlign: 'center' }}>
            正在上传文件...
          </Typography>
        </Box>
      )}

      {mutation.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {(mutation.error as Error).message || '上传失败，请重试'}
        </Alert>
      )}
    </Paper>
  );
}
