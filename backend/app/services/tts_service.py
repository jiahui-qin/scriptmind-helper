"""TTS service — MiMo (Xiaomi) TTS v2.5 via OpenAI SDK.

Per-line synthesis with disk cache (MD5-based) so repeated lines are instant.
Ref: https://platform.xiaomimimo.com/docs/zh-CN/usage-guide/speech-synthesis-v2.5
"""
import os
import hashlib
import base64
from typing import List, Dict, Callable, Optional
from openai import OpenAI
from pydub import AudioSegment
import pysrt
from app.config import settings

MIMO_VOICES = ["mimo_default", "冰糖", "茉莉", "苏打", "白桦", "Mia", "Chloe", "Milo", "Dean"]
PREVIEW_TEXT = "你好，这是一段语音试听，感谢使用台本分析助手。"

os.makedirs("data/preview", exist_ok=True)
os.makedirs("data/tts_cache", exist_ok=True)


def _cache_key(text: str, voice: str) -> str:
    h = hashlib.md5(f"{voice}:{text}".encode()).hexdigest()
    return os.path.join("data", "tts_cache", f"{h}.wav")


def preview_voice(voice: str) -> bytes:
    p = os.path.join("data/preview", f"{voice}.wav")
    if os.path.exists(p):
        with open(p, "rb") as f:
            return f.read()
    wav = _call_mimo_tts(PREVIEW_TEXT, voice)
    with open(p, "wb") as f:
        f.write(wav)
    return wav


def _speed_tone(speed: float) -> str:
    if speed < 0.8:
        return "very slow and calm pace"
    elif speed < 1.0:
        return "slightly slow, gentle pace"
    elif speed > 1.3:
        return "fast and energetic pace"
    return "natural conversational pace"


def _call_mimo_tts(text: str, voice: str = "冰糖", speed: float = 1.0) -> bytes:
    """Call MiMo TTS v2.5, return WAV bytes. Cached by (text, voice) at default speed."""
    if not settings.MIMO_API_KEY or not settings.MIMO_API_KEY.startswith("sk-"):
        raise ValueError("MIMO_API_KEY not configured")

    # Cache hit for default speed
    if speed == 1.0:
        cp = _cache_key(text, voice)
        if os.path.exists(cp):
            with open(cp, "rb") as f:
                return f.read()

    tone = _speed_tone(speed)
    client = OpenAI(api_key=settings.MIMO_API_KEY, base_url=settings.MIMO_API_BASE)
    resp = client.chat.completions.create(
        model="mimo-v2.5-tts",
        messages=[
            {"role": "user", "content": f"{tone}, clear articulation, expressive tone"},
            {"role": "assistant", "content": text},
        ],
        audio={"format": "wav", "voice": voice},
    )
    wav = base64.b64decode(resp.choices[0].message.audio.data)

    # Cache at default speed
    if speed == 1.0:
        with open(cp, "wb") as f:
            f.write(wav)
    return wav


def synthesize_full_script(
    lines: List[Dict],
    role_voice_map: Dict[int, str],
    output_dir: str,
    script_id: int,
    line_gap_ms: int = 300,
    progress_callback: Optional[Callable] = None,
) -> Dict:
    """Per-line synthesis with controllable gap and cache."""
    os.makedirs(output_dir, exist_ok=True)
    segments: List[AudioSegment] = []
    subtitles: List[pysrt.SubRipItem] = []
    failed_lines: List[int] = []
    current_ms = 0
    total = len(lines)
    sample_width = 2
    frame_rate = 24000
    channels = 1

    for i, ln in enumerate(lines):
        role_id = ln.get("role_id")
        voice = role_voice_map.get(role_id, "冰糖")
        speed = ln.get("speech_rate", 1.0)
        text = str(ln.get("content", "")).strip()
        line_no = ln.get("line_number", i + 1)

        if not text:
            continue

        try:
            audio_bytes = _call_mimo_tts(text, voice, speed)
            # Let pydub auto-detect format from WAV header
            seg = AudioSegment.from_file(
                __import__('io').BytesIO(audio_bytes), format="wav"
            )
            # Normalize to 24kHz mono 16-bit for consistent splicing
            if seg.frame_rate != 24000 or seg.channels != 1 or seg.sample_width != 2:
                seg = seg.set_frame_rate(24000).set_channels(1).set_sample_width(2)
            seg = seg.strip_silence(silence_thresh=-40, silence_len=100, padding=30)
        except Exception as e:
            print(f"TTS failed line {line_no}: {e}")
            failed_lines.append(line_no)
            seg = AudioSegment.silent(duration=1000, frame_rate=frame_rate)

        segments.append(seg)
        dur_ms = len(seg)
        subtitles.append(pysrt.SubRipItem(
            index=line_no,
            start=pysrt.SubRipTime(milliseconds=current_ms),
            end=pysrt.SubRipTime(milliseconds=current_ms + dur_ms),
            text=text,
        ))
        current_ms += dur_ms + line_gap_ms

        if progress_callback:
            progress_callback(i + 1, total, failed_lines)

    if not segments:
        raise ValueError("No audio segments generated")

    full = segments[0]
    base_fr = full.frame_rate
    for seg in segments[1:]:
        if line_gap_ms > 0:
            full = full + AudioSegment.silent(duration=line_gap_ms, frame_rate=base_fr)
        full = full + seg

    audio_path = os.path.join(output_dir, f"script_{script_id}_full.wav")
    srt_path = os.path.join(output_dir, f"script_{script_id}_full.srt")
    full.export(audio_path, format="wav")
    pysrt.SubRipFile(items=subtitles).save(srt_path, encoding="utf-8")
    return {"audio_path": audio_path, "srt_path": srt_path, "failed_lines": failed_lines}
