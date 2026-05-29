import { useState } from 'react';
import { Paper, Stack, Typography, Button, Select, MenuItem, Divider } from '@mui/material';
import CancelIcon from '@mui/icons-material/Cancel';
import { type Role } from '../services/api';
import StyleSelector from './StyleSelector';

interface BatchActionBarProps {
  selectedCount: number;
  roles: Role[];
  emotionOptions: string[];
  complexEmotionOptions: string[];
  onClearSelection: () => void;
  onBatchUpdate: (updates: Record<string, any>) => void;
  onQuickTransfer: (fromRoleId: number | null, toRoleId: number | null) => void;
}

export default function BatchActionBar({
  selectedCount, roles, emotionOptions, complexEmotionOptions,
  onClearSelection, onBatchUpdate, onQuickTransfer,
}: BatchActionBarProps) {
  const [batchRoleId, setBatchRoleId] = useState<string>('');
  const [batchEmotion, setBatchEmotion] = useState('');
  const [batchComplex, setBatchComplex] = useState('');
  const [fromRole, setFromRole] = useState<string>('');
  const [toRole, setToRole] = useState<string>('');

  const handleApply = () => {
    const updates: Record<string, any> = {};
    if (batchRoleId) updates.role_id = batchRoleId === '__none__' ? null : Number(batchRoleId);
    if (batchEmotion) updates.emotion_tag = batchEmotion;
    if (batchComplex) updates.complex_emotion = batchComplex;
    if (Object.keys(updates).length > 0) onBatchUpdate(updates);
  };

  return (
    <Paper sx={{ p: 2, mt: 1, border: '1px solid #cfd8e3', borderRadius: 2, bgcolor: '#f8fafc' }}>
      <Stack spacing={1.5}>
        {/* ── 快速转移区（始终可见）────────────────── */}
        <Stack direction="row" alignItems="center" spacing={1.5} flexWrap="wrap" useFlexGap>
          <Typography variant="body2" fontWeight={600} color="text.secondary" sx={{ whiteSpace: 'nowrap' }}>
            ⚡ 快速转移：
          </Typography>
          <Select size="small" value={fromRole} displayEmpty sx={{ minWidth: 100 }}
            onChange={e => setFromRole(e.target.value)}>
            <MenuItem value=""><em>来源角色</em></MenuItem>
            <MenuItem value="__none__">旁白</MenuItem>
            {roles.map(r => <MenuItem key={r.id} value={String(r.id)}>{r.name}</MenuItem>)}
          </Select>
          <Typography variant="body2" color="text.secondary">→</Typography>
          <Select size="small" value={toRole} displayEmpty sx={{ minWidth: 100 }}
            onChange={e => setToRole(e.target.value)}>
            <MenuItem value="" disabled><em>目标角色</em></MenuItem>
            <MenuItem value="__none__">旁白</MenuItem>
            {roles.map(r => <MenuItem key={r.id} value={String(r.id)}>{r.name}</MenuItem>)}
          </Select>
          <Button variant="contained" size="small" disabled={!fromRole || !toRole}
            onClick={() => {
              const from = fromRole === '__none__' ? null : Number(fromRole);
              const to = toRole === '__none__' ? null : Number(toRole);
              if (to !== undefined) onQuickTransfer(from, to);
            }}>
            执行转移
          </Button>
        </Stack>

        {/* ── 批量编辑区（仅在选中时显示）─────────── */}
        {selectedCount > 0 && (
          <>
            <Divider />
            <Stack direction="row" alignItems="center" spacing={1.5} flexWrap="wrap" useFlexGap>
              <Typography variant="body2" fontWeight={600} color="#6366f1" sx={{ whiteSpace: 'nowrap' }}>
                已选 {selectedCount} 行
              </Typography>
              <Button size="small" startIcon={<CancelIcon />} onClick={onClearSelection}>取消选择</Button>
              <Select size="small" value={batchRoleId} displayEmpty sx={{ minWidth: 100 }}
                onChange={e => setBatchRoleId(e.target.value)}>
                <MenuItem value="">角色改为...</MenuItem>
                <MenuItem value="__none__">旁白</MenuItem>
                {roles.map(r => <MenuItem key={r.id} value={String(r.id)}>{r.name}</MenuItem>)}
              </Select>
              <StyleSelector label="基础情绪" value={batchEmotion} options={emotionOptions}
                onChange={setBatchEmotion} />
              <StyleSelector label="复合情绪" value={batchComplex} options={complexEmotionOptions}
                onChange={setBatchComplex} />
              <Button variant="contained" size="small" onClick={handleApply}>应用</Button>
            </Stack>
          </>
        )}
      </Stack>
    </Paper>
  );
}
