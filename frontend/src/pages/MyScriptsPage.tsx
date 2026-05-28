import React, { useEffect, useState, useCallback } from 'react';
import {
  Box, Typography, Container, Paper, Button, Stack,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Chip, IconButton, CircularProgress, Alert, Dialog,
  DialogTitle, DialogContent, DialogContentText, DialogActions,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import DescriptionIcon from '@mui/icons-material/Description';
import { listScripts, deleteScript, type ScriptUploadResponse } from '../services/api';

/** 状态标签配置 */
const STATUS_CONFIG: Record<string, { label: string; color: 'default' | 'primary' | 'success' | 'warning' | 'error' }> = {
  uploaded: { label: '已上传', color: 'default' },
  queued: { label: '排队中', color: 'primary' },
  parsing: { label: '分析中', color: 'primary' },
  analyzing_roles: { label: '分析中', color: 'primary' },
  tagging_emotions: { label: '分析中', color: 'primary' },
  completed: { label: '已完成', color: 'success' },
  failed: { label: '失败', color: 'error' },
};

/** 格式化时间 */
function formatTime(dateStr: string): string {
  try {
    const d = new Date(dateStr);
    return d.toLocaleString('zh-CN', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit',
    });
  } catch {
    return dateStr;
  }
}

export default function MyScriptsPage() {
  const navigate = useNavigate();
  const [scripts, setScripts] = useState<ScriptUploadResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Delete dialog
  const [deleteTarget, setDeleteTarget] = useState<ScriptUploadResponse | null>(null);
  const [deleting, setDeleting] = useState(false);

  /** Fetch scripts list */
  const fetchScripts = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await listScripts();
      const data: ScriptUploadResponse[] = Array.isArray(res.data) ? res.data : [];
      // Sort by created_at descending
      data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      setScripts(data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || '加载台本列表失败');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchScripts();
  }, [fetchScripts]);

  /** Confirm delete */
  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    setDeleting(true);
    try {
      await deleteScript(deleteTarget.id);
      setScripts((prev) => prev.filter((s) => s.id !== deleteTarget.id));
      setDeleteTarget(null);
    } catch (e: any) {
      // ignore — could add toast
    } finally {
      setDeleting(false);
    }
  };

  /** Get status display info */
  const getStatusChip = (status: string) => {
    const config = STATUS_CONFIG[status] || STATUS_CONFIG.uploaded;
    return <Chip label={config.label} color={config.color} size="small" />;
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ py: 4 }}>
        {/* ── 标题栏 ──────────────────────────── */}
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          justifyContent="space-between"
          alignItems={{ xs: 'stretch', sm: 'center' }}
          mb={4}
          gap={2}
        >
          <Box>
            <Typography variant="h5" fontWeight={700} gutterBottom>
              我的台本
            </Typography>
            <Typography variant="body2" color="text.secondary">
              管理已上传的台本文件和分析结果
            </Typography>
          </Box>
          <Button
            variant="text"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/')}
          >
            返回首页
          </Button>
        </Stack>

        {/* ── 加载中 ───────────────────────────── */}
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
            <CircularProgress sx={{ color: '#6366f1' }} />
          </Box>
        )}

        {/* ── 错误 ──────────────────────────────── */}
        {error && !loading && (
          <Alert severity="error" sx={{ borderRadius: 2, mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* ── 空列表 ────────────────────────────── */}
        {!loading && !error && scripts.length === 0 && (
          <Paper
            elevation={0}
            sx={{
              p: 6, textAlign: 'center',
              border: '2px dashed #e2e8f0', borderRadius: 3,
            }}
          >
            <DescriptionIcon sx={{ fontSize: 48, color: '#cbd5e1', mb: 2 }} />
            <Typography variant="h6" color="text.secondary" gutterBottom>
              还没有上传台本
            </Typography>
            <Typography variant="body2" color="text.disabled" sx={{ mb: 3 }}>
              上传台本文件后，即可在此处管理和查看分析结果。
            </Typography>
            <Button
              variant="contained"
              onClick={() => navigate('/')}
              sx={{ borderRadius: 2 }}
            >
              去上传台本
            </Button>
          </Paper>
        )}

        {/* ── 台本列表 ──────────────────────────── */}
        {!loading && !error && scripts.length > 0 && (
          <TableContainer
            component={Paper}
            elevation={0}
            sx={{ border: '1px solid #e2e8f0', borderRadius: 3 }}
          >
            <Table>
              <TableHead>
                <TableRow sx={{ bgcolor: '#f8fafc' }}>
                  <TableCell sx={{ fontWeight: 600 }}>文件名</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>上传时间</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>状态</TableCell>
                  <TableCell sx={{ fontWeight: 600, width: 140 }}>操作</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {scripts.map((script) => (
                  <TableRow
                    key={script.id}
                    hover
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell>
                      <Typography variant="body2" fontWeight={500}>
                        {script.filename}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" color="text.secondary">
                        {formatTime(script.created_at)}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      {getStatusChip(script.status)}
                    </TableCell>
                    <TableCell>
                      <Stack direction="row" spacing={0.5}>
                        <IconButton
                          size="small"
                          color="primary"
                          onClick={() => navigate(`/analysis/${script.id}`)}
                          title="查看分析"
                        >
                          <VisibilityIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => setDeleteTarget(script)}
                          title="删除"
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Stack>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Box>

      {/* ── 删除确认 Dialog ───────────────────── */}
      <Dialog open={!!deleteTarget} onClose={() => setDeleteTarget(null)}>
        <DialogTitle>确认删除</DialogTitle>
        <DialogContent>
          <DialogContentText>
            确定要删除台本「{deleteTarget?.filename}」吗？此操作不可撤销，
            相关的分析结果和语音文件也将一并删除。
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteTarget(null)} disabled={deleting}>
            取消
          </Button>
          <Button
            color="error"
            variant="contained"
            onClick={handleDeleteConfirm}
            disabled={deleting}
          >
            {deleting ? '删除中...' : '确认删除'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
