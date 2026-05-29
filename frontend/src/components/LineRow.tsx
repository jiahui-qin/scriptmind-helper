import { Paper, Typography, Checkbox, Select, MenuItem, Divider } from '@mui/material';
import { type Line, type Role } from '../services/api';
import StyleSelector from './StyleSelector';

interface LineRowProps {
  line: Line;
  roles: Role[];
  selected: boolean;
  onToggleSelect: (lineId: number) => void;
  onUpdateLine: (lineId: number, updates: Record<string, any>) => void;
  onCreateRole: () => void;
  emotionOptions: string[];
  complexEmotionOptions: string[];
}

export default function LineRow({
  line, roles, selected, onToggleSelect, onUpdateLine, onCreateRole, emotionOptions, complexEmotionOptions,
}: LineRowProps) {
  return (
    <Paper
      sx={{
        p: 1, display: 'flex', alignItems: 'center', gap: 1,
        bgcolor: line.role_id ? '#f8fafc' : '#fffbeb',
        border: selected ? '2px solid #6366f1' : '1px solid #e2e8f0',
        borderRadius: 2, flexWrap: 'wrap',
      }}
    >
      <Checkbox size="small" checked={selected} onChange={() => onToggleSelect(line.id)} />
      <Typography variant="caption" color="text.secondary" sx={{ minWidth: 24 }}>#{line.line_number}</Typography>
      <Select
        size="small"
        value={line.role_id === null ? '__none__' : String(line.role_id)}
        onChange={(e) => {
          const val = e.target.value;
          if (val === '__create__') { onCreateRole(); return; }
          onUpdateLine(line.id, { role_id: val === '__none__' ? null : Number(val) });
        }}
        sx={{ minWidth: 90 }}
      >
        <MenuItem value="__none__">旁白</MenuItem>
        <Divider />
        {roles.map(r => <MenuItem key={r.id} value={String(r.id)}>{r.name}</MenuItem>)}
        <Divider />
        <MenuItem value="__create__">
          <Typography variant="body2" color="primary">+ 创建新角色</Typography>
        </MenuItem>
      </Select>
      <Typography variant="body2" sx={{ flex: 1, minWidth: 150, overflow: 'hidden', textOverflow: 'ellipsis' }}>
        {line.content}
      </Typography>
      <StyleSelector
        label="基础情绪"
        value={line.emotion_tag || ''}
        options={emotionOptions}
        onChange={(val) => onUpdateLine(line.id, { emotion_tag: val })}
      />
      <StyleSelector
        label="复合情绪"
        value={line.complex_emotion || ''}
        options={complexEmotionOptions}
        onChange={(val) => onUpdateLine(line.id, { complex_emotion: val })}
      />
    </Paper>
  );
}
