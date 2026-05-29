import { useState } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
  FormControl, InputLabel, Select, MenuItem,
} from '@mui/material';
import { createRole, type Role } from '../services/api';

interface CreateRoleDialogProps {
  open: boolean;
  onClose: () => void;
  onCreated: (role: Role) => void;
  scriptId: number;
}

export default function CreateRoleDialog({ open, onClose, onCreated, scriptId }: CreateRoleDialogProps) {
  const [name, setName] = useState('');
  const [gender, setGender] = useState('未知');
  const [age, setAge] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!name.trim()) return;
    setLoading(true);
    try {
      const res = await createRole(scriptId, { name: name.trim(), gender, age });
      onCreated(res.data as Role);
      setName(''); setGender('未知'); setAge(0);
      onClose();
    } catch (e) { /* ignore */ }
    finally { setLoading(false); }
  };

  const handleClose = () => {
    if (!loading) {
      setName(''); setGender('未知'); setAge(0);
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="xs" fullWidth>
      <DialogTitle>创建新角色</DialogTitle>
      <DialogContent>
        <TextField label="角色名称" value={name} onChange={e => setName(e.target.value)}
          fullWidth size="small" sx={{ mt: 1 }} autoFocus
        />
        <FormControl fullWidth size="small" sx={{ mt: 2 }}>
          <InputLabel>性别</InputLabel>
          <Select value={gender} label="性别" onChange={e => setGender(e.target.value)}>
            <MenuItem value="男">男</MenuItem>
            <MenuItem value="女">女</MenuItem>
            <MenuItem value="未知">未知</MenuItem>
          </Select>
        </FormControl>
        <TextField label="年龄" type="number" value={age} onChange={e => setAge(Number(e.target.value))}
          fullWidth size="small" sx={{ mt: 2 }}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>取消</Button>
        <Button onClick={handleSubmit} variant="contained" disabled={loading || !name.trim()}>创建</Button>
      </DialogActions>
    </Dialog>
  );
}
