import React, { useEffect, useState, useCallback, useRef } from 'react';
import {
  Box, Typography, Paper, LinearProgress, Alert, Button, Checkbox, Stack, Grid,
  Dialog, DialogTitle, DialogContent, DialogActions, Select, MenuItem, Switch, FormControlLabel, Divider,
  FormControl, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, SelectChangeEvent,
} from '@mui/material';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useParams, useNavigate } from 'react-router-dom';
import {
  getAnalysisResult, triggerAnalysis, triggerTTS, getVoices,
  type Role, type Line,
} from '../services/api';
import { updateLine, batchUpdateLines } from '../services/api';
import { BASIC_EMOTIONS, COMPLEX_EMOTIONS } from '../constants/emotions';
import RoleCard from '../components/RoleCard';
import LineRow from '../components/LineRow';
import BatchActionBar from '../components/BatchActionBar';
import CreateRoleDialog from '../components/CreateRoleDialog';

const STATUS_LABELS: Record<string, string> = {
  uploaded: '等待分析',
  queued: '已加入队列',
  parsing: '正在解析台本...',
  analyzing_roles: 'MiMo AI 正在分析角色性格...',
  tagging_emotions: 'MiMo AI 正在标注情感...',
  completed: '分析完成',
  failed: '分析失败',
};

function getStatusIcon(status: string) {
  if (status === 'completed') return String.fromCodePoint(0x2705);
  if (status === 'failed') return String.fromCodePoint(0x274C);
  return String.fromCodePoint(0x1F504);
}

export default function AnalysisPage() {
  const { scriptId } = useParams<{ scriptId: string }>();
  const navigate = useNavigate();
  const [roles, setRoles] = useState<Role[]>([]);
  const [lines, setLines] = useState<Line[]>([]);
  const [status, setStatus] = useState('uploaded');
  const [progress, setProgress] = useState(0);
  const [errorMsg, setErrorMsg] = useState('');
  const [isPolling, setIsPolling] = useState(false);
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // ── 新增 state：选行 / 筛选 / 风格选项 ──
  const [selectedLines, setSelectedLines] = useState<Set<number>>(new Set());
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [createRoleOpen, setCreateRoleOpen] = useState(false);
  const [emotionOptions] = useState<string[]>(BASIC_EMOTIONS);
  const [complexEmotionOptions] = useState<string[]>(COMPLEX_EMOTIONS);

  // Voice mapping state: roleId -> voice
  const [voiceMap, setVoiceMap] = useState<Record<number, string>>({});

  // TTS synthesize dialog
  const [ttsDialogOpen, setTtsDialogOpen] = useState(false);
  const [ttsLoading, setTtsLoading] = useState(false);
  const [includeNarration, setIncludeNarration] = useState(true);
  const [narrationVoice, setNarrationVoice] = useState("冰糖");
  const [ttsError, setTtsError] = useState('');
  const availableVoices = getVoices();

  // Initialize voice map from roles
  useEffect(() => {
    const map: Record<number, string> = {};
    roles.forEach((r) => {
      map[r.id] = r.voice_type || '';
    });
    setVoiceMap((prev) => ({ ...map, ...prev }));
  }, [roles]);

  const fetchResult = useCallback(async () => {
    if (!scriptId) return;
    try {
      const res = await getAnalysisResult(Number(scriptId));
      const data = res.data as any;
      setStatus(data.status || 'uploaded');
      setProgress(data.progress || 0);
      setErrorMsg(data.error_message || '');
      if (data.roles?.length > 0) setRoles(data.roles);
      if (data.lines?.length > 0) setLines(data.lines);
      return data.status;
    } catch (e: any) {
      setErrorMsg(e.message);
      return 'error';
    }
  }, [scriptId]);

  useEffect(() => { fetchResult(); }, [fetchResult]);

  const startPolling = useCallback(() => {
    if (pollingRef.current) return;
    setIsPolling(true);
    pollingRef.current = setInterval(async () => {
      const s = await fetchResult();
      if (s === 'completed' || s === 'failed' || s === 'error') {
        if (pollingRef.current) clearInterval(pollingRef.current);
        pollingRef.current = null;
        setIsPolling(false);
      }
    }, 2000);
  }, [fetchResult]);

  useEffect(() => {
    return () => { if (pollingRef.current) clearInterval(pollingRef.current); };
  }, []);

  const handleTrigger = async () => {
    if (!scriptId) return;
    try {
      setErrorMsg('');
      await triggerAnalysis(Number(scriptId));
      setStatus('queued');
      startPolling();
    } catch (e: any) {
      setErrorMsg(e.message);
    }
  };

  /** Voice change callback for individual RoleCard */
  const handleVoiceChange = (roleId: number, voiceType: string) => {
    setVoiceMap((prev) => ({ ...prev, [roleId]: voiceType }));
  };

  /** Role update callback */
  const handleRoleUpdate = (_roleId: number, _field: string, _value: string) => {
    // RoleCard handles its own save via updateRole API
  };

  /** TTS dialog voice change */
  const handleDialogVoiceChange = (roleId: number) => (e: SelectChangeEvent<string>) => {
    setVoiceMap((prev) => ({ ...prev, [roleId]: e.target.value }));
  };

  /** Trigger TTS synthesis */
  const handleTTSConfirm = async () => {
    if (!scriptId) return;
    setTtsLoading(true);
    setTtsError('');
    try {
      const roleVoiceMap: Record<number, string> = {};
      Object.entries(voiceMap).forEach(([roleId, voice]) => {
        if (voice) roleVoiceMap[Number(roleId)] = voice;
      });
      const res = await triggerTTS(Number(scriptId), roleVoiceMap, includeNarration, narrationVoice);
      const taskId = (res.data as any).task_id;
      setTtsDialogOpen(false);
      navigate(`/result/${taskId}`);
    } catch (e: any) {
      setTtsError(e?.response?.data?.detail || e?.message || 'TTS 合成请求失败');
    } finally {
      setTtsLoading(false);
    }
  };

  // ── 选行 / 筛选 / 行操作回调 ─────────────────

  /** 切换单行选中 */
  const toggleSelectLine = (lineId: number) => {
    setSelectedLines(prev => {
      const next = new Set(prev);
      if (next.has(lineId)) next.delete(lineId); else next.add(lineId);
      return next;
    });
  };

  /** 计算当前筛选后的行 */
  const filteredLines = roleFilter === 'all'
    ? lines
    : lines.filter(l =>
        roleFilter === '0' ? l.role_id === null : l.role_id === Number(roleFilter)
      );

  /** 全选 / 取消全选 */
  const toggleSelectAll = () => {
    if (selectedLines.size === filteredLines.length && filteredLines.length > 0) {
      setSelectedLines(new Set());
    } else {
      setSelectedLines(new Set(filteredLines.map(l => l.id)));
    }
  };

  /** 单行更新 */
  const handleUpdateLine = async (lineId: number, updates: Record<string, any>) => {
    try {
      await updateLine(lineId, updates);
      setLines(prev => prev.map(l => l.id === lineId ? { ...l, ...updates } : l));
    } catch (e) { /* ignore */ }
  };

  /** 批量更新 */
  const handleBatchUpdate = async (updates: Record<string, any>) => {
    try {
      await batchUpdateLines({
        mode: 'by_ids',
        line_ids: Array.from(selectedLines),
        updates,
      } as any);
      setLines(prev => prev.map(l =>
        selectedLines.has(l.id) ? { ...l, ...updates } : l
      ));
      setSelectedLines(new Set());
    } catch (e) { /* ignore */ }
  };

  /** 快速转移 */
  const handleQuickTransfer = async (fromRoleId: number | null, toRoleId: number | null) => {
    if (!scriptId) return;
    try {
      await batchUpdateLines({
        mode: 'by_role',
        script_id: Number(scriptId),
        from_role_id: fromRoleId,
        updates: { role_id: toRoleId },
      } as any);
      fetchResult();
      setSelectedLines(new Set());
    } catch (e) { /* ignore */ }
  };

  /** 创建角色后回调 */
  const handleRoleCreated = (role: Role) => {
    setRoles(prev => [...prev, role]);
  };

  const isRunning = status !== 'completed' && status !== 'failed';

  return (
    <Box sx={{ p: { xs: 2, md: 4 }, maxWidth: 1000, mx: 'auto' }}>
      <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 3 }}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')} size="small">返回</Button>
        <Typography variant="h5" fontWeight={700}>台本分析</Typography>
      </Stack>

      {/* ── 状态面板 ──────────────────────────── */}
      {(isRunning || status === 'completed') && (
        <Paper sx={{ p: 3, mb: 3, border: '1px solid #e2e8f0', borderRadius: 3 }}>
          <Stack spacing={2}>
            <Stack direction="row" alignItems="center" spacing={1}>
              <Typography variant="h6">{getStatusIcon(status)} {STATUS_LABELS[status] || status}</Typography>
            </Stack>
            {isRunning && <>
              <LinearProgress variant={progress > 0 ? 'determinate' : 'indeterminate'} value={progress} sx={{ height: 8, borderRadius: 4 }} />
              <Typography variant="body2" color="text.secondary">{progress > 0 ? progress + '%' : '正在连接 MiMo API...'}</Typography>
            </>}
            {status === 'failed' && <Alert severity="error">{errorMsg ? errorMsg.substring(0, 200) : '分析失败'}</Alert>}
          </Stack>
        </Paper>
      )}

      {/* ── 开始分析按钮 ────────────────────────── */}
      {status === 'uploaded' && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>台本已上传，点击下方按钮开始 AI 分析</Typography>
          <Button variant="contained" size="large" onClick={handleTrigger} disabled={isPolling}
            startIcon={<AutoFixHighIcon />} sx={{ px: 4, py: 1.5, borderRadius: 2 }}>
            {isPolling ? '分析中...' : '开始分析'}
          </Button>
        </Box>
      )}

      {/* ── 角色列表 ────────────────────────────── */}
      {roles.length > 0 && (
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>识别角色 ({roles.length})</Typography>
          <Grid container spacing={2}>
            {roles.map(r => (
              <Grid item xs={12} sm={6} md={4} key={r.id}>
                <RoleCard
                  role={r}
                  voiceType={voiceMap[r.id] || ''}
                  onVoiceChange={handleVoiceChange}
                  onRoleUpdate={handleRoleUpdate}
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* ── 台词列表 ────────────────────────────── */}
      {lines.length > 0 && (
        <Box>
          <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
            <Typography variant="h6" fontWeight={600}>台词列表 ({lines.length} 行)</Typography>
            <Stack direction="row" spacing={1} alignItems="center">
              <Checkbox size="small"
                checked={filteredLines.length > 0 && selectedLines.size === filteredLines.length}
                onChange={toggleSelectAll}
              />
              <Typography variant="caption" color="text.secondary">全选</Typography>
              <Select size="small" value={roleFilter} onChange={e => setRoleFilter(e.target.value)}
                sx={{ minWidth: 100 }}>
                <MenuItem value="all">全部角色</MenuItem>
                {roles.map(r => <MenuItem key={r.id} value={String(r.id)}>{r.name}</MenuItem>)}
              </Select>
            </Stack>
          </Stack>

          <Stack spacing={0.5}>
            {filteredLines.map(line => (
              <LineRow
                key={line.id}
                line={line}
                roles={roles}
                selected={selectedLines.has(line.id)}
                onToggleSelect={toggleSelectLine}
                onUpdateLine={handleUpdateLine}
                onCreateRole={() => setCreateRoleOpen(true)}
                emotionOptions={emotionOptions}
                complexEmotionOptions={complexEmotionOptions}
              />
            ))}
          </Stack>

          <BatchActionBar
            selectedCount={selectedLines.size}
            roles={roles}
            emotionOptions={emotionOptions}
            complexEmotionOptions={complexEmotionOptions}
            onClearSelection={() => setSelectedLines(new Set())}
            onBatchUpdate={handleBatchUpdate}
            onQuickTransfer={handleQuickTransfer}
          />

          <CreateRoleDialog
            open={createRoleOpen}
            onClose={() => setCreateRoleOpen(false)}
            onCreated={handleRoleCreated}
            scriptId={Number(scriptId)}
          />
        </Box>
      )}

      {/* ── TTS 合成按钮（分析完成后显示）────────── */}
      {status === 'completed' && (
        <Box sx={{ textAlign: 'center', mt: 4, mb: 2 }}>
          <Button
            variant="contained"
            size="large"
            onClick={() => setTtsDialogOpen(true)}
            startIcon={<span>{String.fromCodePoint(0x1F399)}</span>}
            sx={{
              px: 5, py: 1.5, borderRadius: 2,
              background: 'linear-gradient(135deg, #8b5cf6, #6366f1)',
              '&:hover': { background: 'linear-gradient(135deg, #7c3aed, #4f46e5)' },
            }}
          >
            生成语音
          </Button>
        </Box>
      )}

      {/* ── TTS 音色选择 Dialog ──────────────────── */}
      <Dialog
        open={ttsDialogOpen}
        onClose={() => setTtsDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle sx={{ fontWeight: 700 }}>
          <span>{String.fromCodePoint(0x1F399)}</span> 角色音色配置
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            为每个角色选择配音音色，确认后将开始语音合成。
          </Typography>
          {ttsError && (
            <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>
              {ttsError}
            </Alert>
          )}
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 600 }}>角色</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>音色</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {roles.map((role) => (
                  <TableRow key={role.id}>
                    <TableCell>
                      <Stack direction="row" spacing={1} alignItems="center">
                        <Box
                          sx={{
                            width: 28, height: 28, borderRadius: 1,
                            bgcolor: '#eef2ff', display: 'flex',
                            alignItems: 'center', justifyContent: 'center',
                          }}
                        >
                          <Typography variant="caption" fontWeight={600} color="#6366f1">
                            {role.name.charAt(0)}
                          </Typography>
                        </Box>
                        <Typography variant="body2" fontWeight={500}>{role.name}</Typography>
                      </Stack>
                    </TableCell>
                    <TableCell>
                      <FormControl fullWidth size="small">
                        <Select
                          value={voiceMap[role.id] || ''}
                          onChange={handleDialogVoiceChange(role.id)}
                          displayEmpty
                        >
                          <MenuItem value="">
                            <Typography variant="body2" color="text.secondary">默认</Typography>
                          </MenuItem>
                          {availableVoices.map((v) => (
                            <MenuItem key={v} value={v}>{v}</MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <Divider sx={{ my: 2 }} />
          <Typography variant="subtitle2" fontWeight={600} gutterBottom>旁白设置</Typography>
          <FormControlLabel
            control={<Switch checked={includeNarration} onChange={(e) => setIncludeNarration(e.target.checked)} size="small" />}
            label="包含旁白"
          />
          {includeNarration && (
            <FormControl fullWidth size="small" sx={{ mt: 0.5 }}>
              <Select value={narrationVoice} onChange={(e) => setNarrationVoice(e.target.value)} displayEmpty>
                {availableVoices.map((v) => (<MenuItem key={v} value={v}>{v}</MenuItem>))}
              </Select>
            </FormControl>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 2, pt: 0 }}>
          <Button onClick={() => setTtsDialogOpen(false)} disabled={ttsLoading}>
            取消
          </Button>
          <Button
            variant="contained"
            onClick={handleTTSConfirm}
            disabled={ttsLoading}
            startIcon={ttsLoading ? undefined : <span>{String.fromCodePoint(0x1F399)}</span>}
          >
            {ttsLoading ? '合成中...' : '确认合成'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
