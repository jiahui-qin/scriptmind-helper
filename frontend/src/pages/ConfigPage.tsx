import React, { useState } from 'react';
import {
  Box, Typography, Paper, TextField, Button, Alert, Stack,
  InputAdornment, IconButton, Divider, Chip, Link, CircularProgress,
} from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import VpnKeyIcon from '@mui/icons-material/VpnKey';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getConfig, getConfigStatus, updateConfig, type ConfigStatus } from '../services/api';

export default function ConfigPage() {
  const qc = useQueryClient();

  // 获取当前配置
  const { data: configData, isLoading: configLoading } = useQuery({
    queryKey: ['config'],
    queryFn: () => getConfig().then((r) => r.data),
  });

  // 获取服务状态
  const { data: statusData, refetch: refetchStatus } = useQuery<ConfigStatus>({
    queryKey: ['configStatus'],
    queryFn: () => getConfigStatus().then((r) => r.data),
  });

  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [verifyResult, setVerifyResult] = useState<'none' | 'success' | 'error'>('none');

  // 初始化 key
  React.useEffect(() => {
    if (configData?.moonshot_api_key) {
      setApiKey(configData.moonshot_api_key);
    }
  }, [configData]);

  // 保存配置
  const saveMutation = useMutation({
    mutationFn: () => updateConfig({ moonshot_api_key: apiKey }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['config'] });
    },
  });

  // 验证连接
  const handleVerify = async () => {
    setVerifyResult('none');
    try {
      await saveMutation.mutateAsync();
      await refetchStatus();
      setVerifyResult('success');
    } catch {
      setVerifyResult('error');
    }
  };

  // 复制到剪贴板
  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text).catch(() => {});
  };

  // 获取 Moonshot API Key 的步骤
  const setupSteps = [
    { step: '1', text: '访问 Moonshot AI 开放平台' },
    { step: '2', text: '注册/登录账号' },
    { step: '3', text: '在控制台创建 API Key' },
    { step: '4', text: '复制 Key 并粘贴到上方输入框' },
  ];

  const statusConfigured = statusData?.moonshot_api_configured ?? false;

  return (
    <Box sx={{ maxWidth: 700, mx: 'auto', py: 2 }}>
      <Typography variant="h5" fontWeight={700} gutterBottom>
        配置中心
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 4 }}>
        配置 API Key 以启用 AI 分析和 TTS 语音合成功能
      </Typography>

      {/* ── 服务状态 ──────────────────────────── */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          mb: 3,
          border: '1px solid #e2e8f0',
          borderRadius: 3,
        }}
      >
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>
          服务状态
        </Typography>
        <Stack direction="row" spacing={2} flexWrap="wrap" useFlexGap>
          <Chip
            icon={statusConfigured ? <CheckCircleIcon /> : <CancelIcon />}
            label={statusConfigured ? 'API Key 已配置' : 'API Key 未配置'}
            color={statusConfigured ? 'success' : 'default'}
            variant={statusConfigured ? 'filled' : 'outlined'}
            size="small"
          />
          <Chip
            label={`数据库: ${statusData?.database_type || '未知'}`}
            variant="outlined"
            size="small"
          />
          <Chip
            label={`最大文件: ${statusData?.max_file_size_mb || 10}MB`}
            variant="outlined"
            size="small"
          />
        </Stack>
        <Box sx={{ mt: 1.5 }}>
          <Button size="small" variant="text" onClick={() => refetchStatus()} sx={{ color: '#64748b' }}>
            刷新状态
          </Button>
        </Box>
      </Paper>

      {/* ── API Key 表单 ──────────────────────── */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          mb: 3,
          border: '1px solid #e2e8f0',
          borderRadius: 3,
        }}
      >
        <Stack direction="row" alignItems="center" spacing={1} mb={2}>
          <VpnKeyIcon sx={{ color: '#6366f1' }} />
          <Typography variant="subtitle1" fontWeight={600}>
            Moonshot API Key
          </Typography>
        </Stack>

        {configLoading ? (
          <CircularProgress size={24} />
        ) : (
          <TextField
            label="API Key"
            type={showKey ? 'text' : 'password'}
            fullWidth
            value={apiKey}
            onChange={(e) => {
              setApiKey(e.target.value);
              setVerifyResult('none');
            }}
            placeholder="sk-..."
            helperText="用于调用 Moonshot AI 大语言模型进行角色分析和情感标注"
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowKey(!showKey)}
                    edge="end"
                    size="small"
                  >
                    {showKey ? <VisibilityOffIcon /> : <VisibilityIcon />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
            sx={{ mb: 2 }}
          />
        )}

        <Stack direction="row" spacing={1.5}>
          <Button
            variant="contained"
            onClick={handleVerify}
            disabled={saveMutation.isPending || !apiKey.trim()}
            sx={{
              fontWeight: 600,
              borderRadius: 2,
            }}
          >
            {saveMutation.isPending ? '保存中...' : '保存并验证'}
          </Button>
          <Button
            variant="outlined"
            onClick={() => saveMutation.mutate()}
            disabled={saveMutation.isPending || !apiKey.trim()}
            sx={{ borderRadius: 2, borderColor: '#e2e8f0', color: '#475569' }}
          >
            仅保存
          </Button>
        </Stack>

        {/* 验证结果 */}
        {verifyResult === 'success' && (
          <Alert severity="success" sx={{ mt: 2, borderRadius: 2 }}>
            API Key 验证成功！AI 分析和 TTS 功能已就绪。
          </Alert>
        )}
        {verifyResult === 'error' && (
          <Alert severity="warning" sx={{ mt: 2, borderRadius: 2 }}>
            API Key 已保存，但验证失败。请检查 Key 是否正确，并确保网络连接正常。
          </Alert>
        )}
        {saveMutation.isSuccess && verifyResult === 'none' && (
          <Alert severity="success" sx={{ mt: 2, borderRadius: 2 }}>
            配置已保存成功。
          </Alert>
        )}
        {saveMutation.isError && (
          <Alert severity="error" sx={{ mt: 2, borderRadius: 2 }}>
            保存失败: {(saveMutation.error as Error)?.message || '未知错误'}
          </Alert>
        )}
      </Paper>

      {/* ── 使用说明 ──────────────────────────── */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          border: '1px solid #e2e8f0',
          borderRadius: 3,
        }}
      >
        <Stack direction="row" alignItems="center" spacing={1} mb={2}>
          <InfoOutlinedIcon sx={{ color: '#6366f1' }} />
          <Typography variant="subtitle1" fontWeight={600}>
            如何获取 Moonshot API Key
          </Typography>
        </Stack>

        <Stack spacing={1.5} mb={3}>
          {setupSteps.map((item) => (
            <Stack key={item.step} direction="row" spacing={1.5} alignItems="flex-start">
              <Box
                sx={{
                  width: 24,
                  height: 24,
                  borderRadius: '50%',
                  bgcolor: '#eef2ff',
                  color: '#6366f1',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  flexShrink: 0,
                  mt: 0.25,
                }}
              >
                {item.step}
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.8 }}>
                {item.text}
              </Typography>
            </Stack>
          ))}
        </Stack>

        <Divider sx={{ mb: 2 }} />

        <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.8 }}>
          Moonshot AI 开放平台地址：
        </Typography>
        <Stack direction="row" spacing={1} alignItems="center">
          <Link
            href="https://platform.moonshot.cn"
            target="_blank"
            rel="noopener noreferrer"
            underline="hover"
            sx={{ fontWeight: 500, color: '#6366f1' }}
          >
            https://platform.moonshot.cn
          </Link>
          <IconButton size="small" onClick={() => handleCopy('https://platform.moonshot.cn')}>
            <ContentCopyIcon sx={{ fontSize: 14, color: '#94a3b8' }} />
          </IconButton>
        </Stack>
        <Typography variant="caption" color="text.disabled" sx={{ mt: 1, display: 'block' }}>
          提示: API Key 以 sk- 开头，请妥善保管，不要分享给他人。
        </Typography>
      </Paper>
    </Box>
  );
}
