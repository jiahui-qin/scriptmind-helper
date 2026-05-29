import React, { useState, useEffect } from 'react';
import {
  Card, CardContent, Typography, IconButton, Collapse, Chip, Box,
  Select, MenuItem, FormControl, InputLabel, TextField, Stack,
  SelectChangeEvent, CircularProgress,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import MaleIcon from '@mui/icons-material/Male';
import FemaleIcon from '@mui/icons-material/Female';
import PersonIcon from '@mui/icons-material/Person';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import { type Role, getVoices, updateRole } from '../services/api';
import StyleSelector from './StyleSelector';
import { TONE_STYLES, VOICE_COLORS, PERSONA_ACCENTS, DIALECTS, ROLEPLAYS, SINGING_STYLES } from '../constants/emotions';

interface RoleCardProps {
  role: Role;
  voiceType: string;
  onVoiceChange: (roleId: number, voiceType: string) => void;
  onRoleUpdate: (roleId: number, field: string, value: string) => void;
  onVoiceOptions?: { id: string; name: string; gender: string }[];
}

/** 根据性别返回对应图标 */
function GenderIcon({ gender }: { gender: string }) {
  const g = gender?.toLowerCase() || '';
  if (g === '男' || g === 'male') return <MaleIcon sx={{ color: '#3b82f6', fontSize: 18 }} />;
  if (g === '女' || g === 'female') return <FemaleIcon sx={{ color: '#ec4899', fontSize: 18 }} />;
  return <PersonIcon sx={{ color: '#94a3b8', fontSize: 18 }} />;
}

/** 性格标签颜色映射 */
function getPersonalityColor(personality: string): string {
  const map: Record<string, string> = {
    开朗: '#22c55e', 温柔: '#f59e0b', 沉稳: '#6366f1',
    活泼: '#ec4899', 冷静: '#3b82f6', 严肃: '#64748b',
    热情: '#ef4444', 内敛: '#8b5cf6', 勇敢: '#f97316',
    善良: '#10b981', 机智: '#06b6d4', 冷酷: '#6b7280',
    天真: '#fbbf24', 成熟: '#78716c',
  };
  return map[personality] || '#94a3b8';
}

export default function RoleCard({
  role,
  voiceType,
  onVoiceChange,
  onRoleUpdate,
}: RoleCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [editing, setEditing] = useState(false);
  const [editName, setEditName] = useState(role.name);
  const [editPersonality, setEditPersonality] = useState(role.personality || '');

  // Voice state
  const [voiceOptions, setVoiceOptions] = useState<string[]>([]);
  const [voiceLoading, setVoiceLoading] = useState(false);
  const [voiceSaving, setVoiceSaving] = useState(false);
  const [voiceError, setVoiceError] = useState('');

  // Load available voices on mount
  useEffect(() => {
    try {
      const voices = getVoices();
      setVoiceOptions(voices);
    } catch {
      // getVoices is synchronous (returns static array), won't throw
    }
  }, []);

  /** Handle voice selection change — save to backend automatically */
  const handleVoiceChange = async (e: SelectChangeEvent<string>) => {
    const newVoice = e.target.value;
    setVoiceSaving(true);
    setVoiceError('');

    try {
      await updateRole(role.id, { voice_type: newVoice });
      onVoiceChange(role.id, newVoice);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || '保存音色失败';
      setVoiceError(msg);
    } finally {
      setVoiceSaving(false);
    }
  };

  const startEditing = () => {
    setEditName(role.name);
    setEditPersonality(role.personality || '');
    setEditing(true);
  };

  const saveEditing = () => {
    onRoleUpdate(role.id, 'name', editName);
    onRoleUpdate(role.id, 'personality', editPersonality);
    setEditing(false);
  };

  const cancelEditing = () => {
    setEditing(false);
    setEditName(role.name);
    setEditPersonality(role.personality || '');
  };

  const personalityTraits = (role.personality || '')
    .split(/[,，、]/)
    .map((s) => s.trim())
    .filter(Boolean);

  const ageDisplay = role.age_range || (role.age ? `${role.age}岁` : '未知');

  return (
    <Card
      elevation={0}
      sx={{
        border: '1px solid #e2e8f0',
        borderRadius: 3,
        transition: 'all 0.2s ease',
        '&:hover': { boxShadow: '0 4px 20px rgba(0,0,0,0.06)' },
      }}
    >
      <CardContent sx={{ p: 3, '&:last-child': { pb: 3 } }}>
        {/* ── 头部信息 ──────────────────────────── */}
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={1.5}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <Box
              sx={{
                width: 44,
                height: 44,
                borderRadius: 2,
                bgcolor: '#eef2ff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <RecordVoiceOverIcon sx={{ color: '#6366f1' }} />
            </Box>
            <Box>
              {editing ? (
                <TextField
                  size="small"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  sx={{ width: 140 }}
                  autoFocus
                />
              ) : (
                <Typography variant="h6" fontWeight={600} sx={{ fontSize: '1.1rem' }}>
                  {role.name}
                </Typography>
              )}
              <Stack direction="row" spacing={0.5} alignItems="center">
                <GenderIcon gender={role.gender || ''} />
                <Typography variant="caption" color="text.secondary">
                  {role.gender || '未知'} · {ageDisplay}
                </Typography>
              </Stack>
            </Box>
          </Stack>
          <IconButton
            size="small"
            onClick={() => setExpanded(!expanded)}
            sx={{ color: '#94a3b8' }}
          >
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </Stack>

        {/* ── 性格标签 ──────────────────────────── */}
        {editing ? (
          <TextField
            size="small"
            fullWidth
            value={editPersonality}
            onChange={(e) => setEditPersonality(e.target.value)}
            placeholder="输入性格描述，用逗号分隔"
            sx={{ mb: 1.5 }}
          />
        ) : (
          <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap mb={1.5}>
            {personalityTraits.length > 0 ? (
              personalityTraits.map((trait, idx) => (
                <Chip
                  key={idx}
                  label={trait}
                  size="small"
                  sx={{
                    bgcolor: getPersonalityColor(trait) + '18',
                    color: getPersonalityColor(trait),
                    fontWeight: 500,
                    fontSize: '0.75rem',
                    borderRadius: 1,
                  }}
                />
              ))
            ) : (
              <Typography variant="caption" color="text.disabled">
                暂无性格标注
              </Typography>
            )}
          </Stack>
        )}

        {/* ── 编辑按钮 ──────────────────────────── */}
        <Stack direction="row" spacing={1} mb={2}>
          {editing ? (
            <>
              <Chip label="保存" size="small" color="primary" onClick={saveEditing} clickable />
              <Chip label="取消" size="small" variant="outlined" onClick={cancelEditing} clickable />
            </>
          ) : (
            <Chip
              label="编辑角色设定"
              size="small"
              variant="outlined"
              onClick={startEditing}
              clickable
              sx={{ borderColor: '#cbd5e1' }}
            />
          )}
          {role.line_count !== undefined && (
            <Chip
              label={`${role.line_count} 句台词`}
              size="small"
              variant="outlined"
              sx={{ borderColor: '#e2e8f0', color: '#94a3b8' }}
            />
          )}
        </Stack>

        {/* ── 音色选择 ──────────────────────────── */}
        <FormControl fullWidth size="small" error={!!voiceError}>
          <InputLabel>音色选择</InputLabel>
          <Select
            value={voiceType || ''}
            label="音色选择"
            onChange={handleVoiceChange}
            disabled={voiceSaving}
            sx={{ borderRadius: 2 }}
            endAdornment={
              voiceSaving ? (
                <CircularProgress size={20} sx={{ mr: 3 }} />
              ) : null
            }
          >
            <MenuItem value="">
              <Typography variant="body2" color="text.secondary">默认音色</Typography>
            </MenuItem>
            {voiceOptions.map((v) => (
              <MenuItem key={v} value={v}>
                <Stack direction="row" spacing={1} alignItems="center">
                  <PersonIcon fontSize="small" sx={{ color: '#94a3b8' }} />
                  <Typography variant="body2">{v}</Typography>
                </Stack>
              </MenuItem>
            ))}
          </Select>
          {voiceError && (
            <Typography variant="caption" color="error" sx={{ mt: 0.5 }}>
              {voiceError}
            </Typography>
          )}
        </FormControl>

        {/* ── 展开详细描述 ──────────────────────── */}
        <Collapse in={expanded}>
          <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid #f1f5f9' }}>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              角色详细描述
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.8 }}>
              {role.description || '暂无详细描述。完成 AI 分析后将自动生成角色描述。'}
            </Typography>
            {role.voice_type && (
              <Box sx={{ mt: 1.5 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  推荐的音色类型
                </Typography>
                <Chip
                  label={role.voice_type}
                  size="small"
                  color="secondary"
                  variant="outlined"
                />
              </Box>
            )}

            {/* ── 人物风格属性（可编辑）─── */}
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>人物风格属性</Typography>
              <Stack spacing={1}>
                <StyleSelector label="整体语调" value={role.tone_style || ''} options={TONE_STYLES}
                  onChange={(val) => { updateRole(role.id, { tone_style: val }); }} />
                <StyleSelector label="音色定位" value={role.voice_color || ''} options={VOICE_COLORS}
                  onChange={(val) => { updateRole(role.id, { voice_color: val }); }} />
                <StyleSelector label="人设腔调" value={role.persona_accent || ''} options={PERSONA_ACCENTS}
                  onChange={(val) => { updateRole(role.id, { persona_accent: val }); }} />
                <StyleSelector label="方言" value={role.dialect || ''} options={DIALECTS}
                  onChange={(val) => { updateRole(role.id, { dialect: val }); }} />
                <StyleSelector label="角色扮演" value={role.roleplay || ''} options={ROLEPLAYS}
                  onChange={(val) => { updateRole(role.id, { roleplay: val }); }} />
                <StyleSelector label="唱歌" value={role.singing || ''} options={SINGING_STYLES}
                  onChange={(val) => { updateRole(role.id, { singing: val }); }} />
              </Stack>
            </Box>
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
}
