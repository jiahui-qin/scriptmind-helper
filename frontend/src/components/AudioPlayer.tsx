import React, { useRef, useState, useEffect, useCallback } from 'react';
import {
  Box, Typography, IconButton, Stack, Slider, Button, Paper, Tooltip,
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import AudioFileIcon from '@mui/icons-material/AudioFile';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import VolumeOffIcon from '@mui/icons-material/VolumeOff';
import Replay10Icon from '@mui/icons-material/Replay10';
import Forward30Icon from '@mui/icons-material/Forward30';
import SubtitlesIcon from '@mui/icons-material/Subtitles';
import AudioFileIcon from '@mui/icons-material/AudioFile';

interface AudioPlayerProps {
  audioUrl: string;
  srtUrl?: string;
  title?: string;
}

/** 格式化时间 (秒 → mm:ss) */
function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

export default function AudioPlayer({ audioUrl, srtUrl, title }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);

  // 播放/暂停
  const togglePlay = useCallback(() => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play().catch(() => {});
    }
    setIsPlaying(!isPlaying);
  }, [isPlaying]);

  // 时间更新
  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  // 加载完成
  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  // 播放结束
  const handleEnded = () => {
    setIsPlaying(false);
    setCurrentTime(0);
    if (audioRef.current) {
      audioRef.current.currentTime = 0;
    }
  };

  // 进度条拖动
  const handleSeek = (_e: Event, value: number | number[]) => {
    const time = value as number;
    setCurrentTime(time);
    if (audioRef.current) {
      audioRef.current.currentTime = time;
    }
  };

  // 音量控制
  const handleVolumeChange = (_e: Event, value: number | number[]) => {
    const vol = value as number;
    setVolume(vol);
    if (audioRef.current) {
      audioRef.current.volume = vol;
    }
    if (vol > 0) setIsMuted(false);
  };

  // 静音切换
  const toggleMute = () => {
    if (!audioRef.current) return;
    if (isMuted) {
      audioRef.current.volume = volume || 1;
      setIsMuted(false);
    } else {
      audioRef.current.volume = 0;
      setIsMuted(true);
    }
  };

  // 快进/快退
  const skip = (sec: number) => {
    if (!audioRef.current) return;
    audioRef.current.currentTime = Math.min(
      Math.max(audioRef.current.currentTime + sec, 0),
      duration
    );
  };

  // 下载
  const handleDownload = (url: string, filename: string) => {
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  // 键盘快捷键
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' && e.target === document.body) {
        e.preventDefault();
        togglePlay();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [togglePlay]);

  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        border: '1px solid #e2e8f0',
        borderRadius: 3,
        bgcolor: '#fafbff',
      }}
    >
      {title && (
        <Typography variant="subtitle2" fontWeight={600} gutterBottom>
          {title}
        </Typography>
      )}

      {/* 隐藏的 audio 元素 */}
      <audio
        ref={audioRef}
        src={audioUrl}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={handleEnded}
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        preload="metadata"
      />

      {/* ── 进度条 ──────────────────────────── */}
      <Stack direction="row" spacing={1.5} alignItems="center" sx={{ mb: 1 }}>
        <Typography variant="caption" color="text.secondary" sx={{ minWidth: 40, textAlign: 'right' }}>
          {formatTime(currentTime)}
        </Typography>
        <Slider
          value={currentTime}
          max={duration || 0}
          onChange={handleSeek}
          size="small"
          sx={{
            color: '#6366f1',
            '& .MuiSlider-thumb': {
              width: 14,
              height: 14,
              '&:hover': { boxShadow: '0 0 0 8px rgba(99,102,241,0.12)' },
            },
            '& .MuiSlider-rail': { bgcolor: '#e2e8f0' },
          }}
        />
        <Typography variant="caption" color="text.secondary" sx={{ minWidth: 40 }}>
          {formatTime(duration)}
        </Typography>
      </Stack>

      {/* ── 控制按钮 ─────────────────────────── */}
      <Stack direction="row" alignItems="center" justifyContent="center" spacing={1} sx={{ mb: 2 }}>
        <Tooltip title="后退 10 秒">
          <IconButton size="small" onClick={() => skip(-10)}>
            <Replay10Icon />
          </IconButton>
        </Tooltip>

        <IconButton
          onClick={togglePlay}
          sx={{
            width: 56,
            height: 56,
            bgcolor: '#6366f1',
            color: 'white',
            '&:hover': { bgcolor: '#4f46e5' },
          }}
        >
          {isPlaying ? <PauseIcon sx={{ fontSize: 32 }} /> : <PlayArrowIcon sx={{ fontSize: 32 }} />}
        </IconButton>

        <Tooltip title="快进 30 秒">
          <IconButton size="small" onClick={() => skip(30)}>
            <Forward30Icon />
          </IconButton>
        </Tooltip>

        {/* 音量控制 */}
        <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
          <IconButton size="small" onClick={toggleMute}>
            {isMuted || volume === 0 ? <VolumeOffIcon /> : <VolumeUpIcon />}
          </IconButton>
          <Slider
            value={isMuted ? 0 : volume}
            min={0}
            max={1}
            step={0.05}
            onChange={handleVolumeChange}
            size="small"
            sx={{ width: 80, color: '#6366f1' }}
          />
        </Box>
      </Stack>

      {/* ── 下载按钮 ─────────────────────────── */}
      <Stack direction="row" spacing={1} justifyContent="center">
        <Button
          variant="outlined"
          size="small"
          startIcon={<AudioFileIcon />}
          onClick={() => handleDownload(audioUrl, `${title || 'audio'}.wav`)}
          sx={{ borderRadius: 2, borderColor: '#e2e8f0', color: '#475569' }}
        >
          下载 WAV
        </Button>
        {srtUrl && (
          <Button
            variant="outlined"
            size="small"
            startIcon={<SubtitlesIcon />}
            onClick={() => handleDownload(srtUrl, `${title || 'subtitle'}.srt`)}
            sx={{ borderRadius: 2, borderColor: '#e2e8f0', color: '#475569' }}
          >
            下载 SRT 字幕
          </Button>
        )}
      </Stack>

      {/* 快捷键提示 */}
      <Typography variant="caption" color="text.disabled" sx={{ mt: 1.5, display: 'block', textAlign: 'center' }}>
        按空格键播放/暂停
      </Typography>
    </Paper>
  );
}
