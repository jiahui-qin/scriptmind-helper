import React, { useState } from 'react';
import {
  Card, CardContent, Typography, IconButton, Collapse, Chip, Box,
  Select, MenuItem, FormControl, InputLabel, TextField, Stack,
  SelectChangeEvent,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import MaleIcon from '@mui/icons-material/Male';
import FemaleIcon from '@mui/icons-material/Female';
import PersonIcon from '@mui/icons-material/Person';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import { type Role } from '../services/api';

/** 可用的音色列表（与 MiMo TTS 对应） */
const VOICE_OPTIONS: { id: string; name: string; gender: string }[] = [
  { id: 'default', name: '默认音色', gender: 'any' },
  { id: 'zh-CN-XiaoxiaoNeural', name: '晓晓（女声·温柔）', gender: 'female' },
  { id: 'zh-CN-YunxiNeural', name: '云希（男声·叙事）', gender: 'male' },
  { id: 'zh-CN-YunyangNeural', name: '云扬（男声·新闻）', gender: 'male' },
  { id: 'zh-CN-XiaohanNeural', name: '晓涵（女声·活泼）', gender: 'female' },
  { id: 'zh-CN-XiaomoNeural', name: '晓墨（女声·沉稳）', gender: 'female' },
  { id: 'zh-CN-XiaoxuanNeural', name: '晓萱（女声·自信）', gender: 'female' },
  { id: 'zh-CN-XiaoruiNeural', name: '晓睿（女声·成熟）', gender: 'female' },
  { id: 'zh-CN-YunjianNeural', name: '云健（男声·运动）', gender: 'male' },
];

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

  const handleVoiceChange = (e: SelectChangeEvent<string>) => {
    onVoiceChange(role.id, e.target.value);
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
        <FormControl fullWidth size="small">
          <InputLabel>音色选择</InputLabel>
          <Select
            value={voiceType || 'default'}
            label="音色选择"
            onChange={handleVoiceChange}
            sx={{ borderRadius: 2 }}
          >
            {VOICE_OPTIONS.map((v) => (
              <MenuItem key={v.id} value={v.id}>
                <Stack direction="row" spacing={1} alignItems="center">
                  {v.gender === 'male' ? (
                    <MaleIcon fontSize="small" sx={{ color: '#3b82f6' }} />
                  ) : v.gender === 'female' ? (
                    <FemaleIcon fontSize="small" sx={{ color: '#ec4899' }} />
                  ) : (
                    <PersonIcon fontSize="small" sx={{ color: '#94a3b8' }} />
                  )}
                  <Typography variant="body2">{v.name}</Typography>
                </Stack>
              </MenuItem>
            ))}
          </Select>
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
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
}
