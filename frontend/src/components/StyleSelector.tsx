import { useState, useEffect } from 'react';
import { Autocomplete, TextField } from '@mui/material';

interface StyleSelectorProps {
  label: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
  size?: 'small' | 'medium';
  disabled?: boolean;
}

export default function StyleSelector({
  label, value, options, onChange, size = 'small', disabled = false,
}: StyleSelectorProps) {
  const [local, setLocal] = useState(value || '');

  useEffect(() => {
    setLocal(value || '');
  }, [value]);

  return (
    <Autocomplete
      freeSolo
      size={size}
      disabled={disabled}
      value={local}
      options={options}
      onInputChange={(_e, newInputValue, reason) => {
        setLocal(newInputValue);
        if (reason === 'reset') {
          onChange(newInputValue);
        }
      }}
      onChange={(_e, newValue) => {
        const v = newValue || '';
        setLocal(v);
        onChange(v);
      }}
      onBlur={() => {
        if (local !== (value || '')) {
          onChange(local);
        }
      }}
      renderInput={(params) => <TextField {...params} label={label} size={size} />}
      sx={{ minWidth: 100 }}
    />
  );
}
