import React, { useState } from 'react';
import {
  Box, Typography, Paper, TextField, Button, Alert, Stack,
  IconButton, InputAdornment, Link, Divider,
} from '@mui/material';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { useMutation } from '@tanstack/react-query';
import { updateConfig, getConfigStatus } from '../services/api';
import { useQuery } from '@tanstack/react-query';

export default function ConfigPage() {
  const [key, setKey] = useState('');
  const [showKey, setShowKey] = useState(false);

  const { data: status } = useQuery({
    queryKey: ['config-status'],
    queryFn: () => getConfigStatus().then(r => r.data),
  });

  const saveMutation = useMutation({
    mutationFn: () => updateConfig({ mimo_api_key: key }),
  });

  const handleSave = () => saveMutation.mutate();

  return (
    <Box sx={{ maxWidth: 640, mx: 'auto', py: 4 }}>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        配置中心
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        配置 MiMo API Key 以启用 AI 角色分析和 TTS 语音合成功能
      </Typography>

      {/* API Key Section */}
      <Paper elevation={0} sx={{ p: 3, mb: 3, border: '1px solid #e2e8f0', borderRadius: 3 }}>
        <Stack spacing={2.5}>
          <Box>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
              MiMo API Key
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5 }}>
              用于调用 MiMo（小米）大语言模型进行角色分析和情感标注，以及 TTS 语音合成
            </Typography>
            <TextField
              fullWidth
              type={showKey ? 'text' : 'password'}
              value={key}
              onChange={e => setKey(e.target.value)}
              placeholder="sk-..."
              size="small"
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => setShowKey(!showKey)} edge="end" size="small">
                      {showKey ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Box>

          <Button
            variant="contained"
            onClick={handleSave}
            disabled={!key || saveMutation.isPending}
            sx={{ py: 1.2 }}
          >
            {saveMutation.isPending ? '保存中...' : '保存配置'}
          </Button>

          {saveMutation.isSuccess && (
            <Alert severity="success" icon={<CheckCircleIcon />}>
              配置已保存
            </Alert>
          )}
          {saveMutation.isError && (
            <Alert severity="error">
              保存失败：{(saveMutation.error as Error)?.message || '未知错误'}
            </Alert>
          )}
        </Stack>
      </Paper>

      {/* Status Card */}
      {status && (
        <Paper elevation={0} sx={{ p: 3, mb: 3, border: '1px solid #e2e8f0', borderRadius: 3 }}>
          <Typography variant="subtitle1" fontWeight={600} gutterBottom>
            服务状态
          </Typography>
          <Stack spacing={1}>
            <StatusRow label="MiMo API" ok={status.mimo_api_configured} />
            <StatusRow label="角色分析" ok={status.features?.analysis} />
            <StatusRow label="TTS 合成" ok={status.features?.tts} />
            <StatusRow label="文件上传" ok={status.features?.upload} />
          </Stack>
        </Paper>
      )}

      {/* Help Section */}
      <Paper elevation={0} sx={{ p: 3, border: '1px solid #e2e8f0', borderRadius: 3 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>
          如何获取 MiMo API Key
        </Typography>
        <Stack spacing={1} sx={{ color: 'text.secondary', fontSize: '0.9rem' }}>
          <Typography variant="body2">1. 访问{' '}
            <Link href="https://platform.xiaomimimo.com" target="_blank" rel="noopener">
              MiMo 开放平台
            </Link>
          </Typography>
          <Typography variant="body2">2. 注册/登录小米账号</Typography>
          <Typography variant="body2">3. 在控制台创建 API Key</Typography>
          <Typography variant="body2">4. 将 Key 粘贴到上方输入框并保存</Typography>
        </Stack>
        <Divider sx={{ my: 2 }} />
        <Typography variant="caption" color="text.secondary">
          MiMo API 使用 OpenAI 兼容格式，支持 mimo-v2.5-pro（对话）和 mimo-v2.5-tts（语音合成）模型。
        </Typography>
      </Paper>
    </Box>
  );
}

function StatusRow({ label, ok }: { label: string; ok?: boolean }) {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <Box
        sx={{
          width: 10, height: 10, borderRadius: '50%',
          bgcolor: ok ? '#22c55e' : '#e2e8f0',
        }}
      />
      <Typography variant="body2">{label}</Typography>
      <Typography variant="body2" sx={{ ml: 'auto', color: ok ? '#22c55e' : '#94a3b8' }}>
        {ok ? '已连接' : '未配置'}
      </Typography>
    </Box>
  );
}
