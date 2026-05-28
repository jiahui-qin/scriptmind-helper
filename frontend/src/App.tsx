import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider, createTheme, CssBaseline, Container, AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AnalysisPage from './pages/AnalysisPage';
import ResultPage from './pages/ResultPage';
import ConfigPage from './pages/ConfigPage';

const queryClient = new QueryClient({ defaultOptions: { queries: { retry: 1, staleTime: 30000 } } });

const theme = createTheme({
  palette: { mode: 'light', primary: { main: '#6366f1' }, secondary: { main: '#ec4899' }, background: { default: '#f8fafc' } },
  typography: { fontFamily: '"Roboto", "Noto Sans SC", sans-serif' },
});

function NavBar() {
  const navigate = useNavigate();
  return (
    <AppBar position="static" elevation={0} sx={{ bgcolor: 'white', borderBottom: '1px solid #e2e8f0' }}>
      <Toolbar>
        <Typography variant="h6" sx={{ fontWeight: 700, color: '#6366f1', cursor: 'pointer', flexGrow: 1 }} onClick={() => navigate('/')}>
          ScriptMind AI
        </Typography>
        <Button sx={{ color: '#64748b' }} onClick={() => navigate('/')}>首页</Button>
        <Button sx={{ color: '#64748b' }} onClick={() => navigate('/config')}>配置</Button>
      </Toolbar>
    </AppBar>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <NavBar />
          <Container maxWidth="lg" sx={{ py: 4 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/analysis/:scriptId" element={<AnalysisPage />} />
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
