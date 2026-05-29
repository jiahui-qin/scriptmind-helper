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
  return (
    <Autocomplete
      freeSolo
      size={size}
      disabled={disabled}
      value={value || ''}
      options={options}
      onChange={(_e, newValue) => { if (newValue) onChange(newValue); }}
      onInputChange={(_e, newInputValue) => { onChange(newInputValue); }}
      renderInput={(params) => <TextField {...params} label={label} size={size} />}
      sx={{ minWidth: 100 }}
    />
  );
}
