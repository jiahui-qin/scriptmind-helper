import { useState, useMemo } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider, createTheme, CssBaseline, Container, AppBar, Toolbar, Typography, Button, IconButton } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import HomePage from './pages/HomePage';
import AnalysisPage from './pages/AnalysisPage';
import ResultPage from './pages/ResultPage';
import ConfigPage from './pages/ConfigPage';
import MyScriptsPage from './pages/MyScriptsPage';

const queryClient = new QueryClient({ defaultOptions: { queries: { retry: 1, staleTime: 30000 } } });

function NavBar({ dark, onToggle }: { dark: boolean; onToggle: () => void }) {
  const navigate = useNavigate();
  return (
    <AppBar position="static" elevation={0} sx={{ bgcolor: dark ? '#1e1e2e' : 'white', borderBottom: `1px solid ${dark ? '#313244' : '#e2e8f0'}` }}>
      <Toolbar>
        <Typography variant="h6" sx={{ fontWeight: 700, color: '#6366f1', cursor: 'pointer', flexGrow: 1 }} onClick={() => navigate('/')}>
          ScriptMind AI
        </Typography>
        <Button sx={{ color: dark ? '#cdd6f4' : '#64748b' }} onClick={() => navigate('/')}>首页</Button>
        <Button sx={{ color: dark ? '#cdd6f4' : '#64748b' }} onClick={() => navigate('/my-scripts')}>我的台本</Button>
        <Button sx={{ color: dark ? '#cdd6f4' : '#64748b' }} onClick={() => navigate('/config')}>配置</Button>
        <IconButton onClick={onToggle} sx={{ ml: 1, color: dark ? '#f9e2af' : '#64748b' }}>
          {dark ? <LightModeIcon /> : <DarkModeIcon />}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}

function App() {
  const [dark, setDark] = useState(false);

  const theme = useMemo(() => createTheme({
    palette: {
      mode: dark ? 'dark' : 'light',
      primary: { main: '#6366f1' },
      secondary: { main: '#ec4899' },
      background: dark
        ? { default: '#11111b', paper: '#1e1e2e' }
        : { default: '#f8fafc', paper: '#ffffff' },
    },
    typography: { fontFamily: '"Roboto", "Noto Sans SC", sans-serif' },
  }), [dark]);

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <NavBar dark={dark} onToggle={() => setDark(d => !d)} />
          <Container maxWidth="lg" sx={{ py: 4 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/analysis/:scriptId" element={<AnalysisPage />} />
              <Route path="/my-scripts" element={<MyScriptsPage />} />
              <Route path="/result/:taskId" element={<ResultPage />} />
              <Route path="/config" element={<ConfigPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Container>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
