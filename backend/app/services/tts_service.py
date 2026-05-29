"""TTS service — MiMo (Xiaomi) TTS v2.5 via OpenAI SDK.

Ref: https://platform.xiaomimimo.com/docs/zh-CN/usage-guide/speech-synthesis-v2.5
"""
import os
import base64
from typing import List, Dict, Tuple
from openai import OpenAI
from pydub import AudioSegment
import pysrt
from app.config import settings

# Supported MiMo TTS voices
MIMO_VOICES = ["mimo_default", "冰糖", "茉莉", "苏打", "白桦", "Mia", "Chloe", "Milo", "Dean"]

# Preview text for voice sampling
PREVIEW_TEXT = "你好，这是一段语音试听，感谢使用台本分析助手。"


def _get_preview_cache_path(voice: str) -> str:
    """Return cache path for a voice preview file."""
    os.makedirs("data/preview", exist_ok=True)
    return os.path.join("data/preview", f"{voice}.wav")


def preview_voice(voice: str) -> bytes:
    """Generate (or retrieve cached) a short voice preview as WAV bytes."""
    cache_path = _get_preview_cache_path(voice)
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return f.read()

    wav_bytes = _call_mimo_tts(PREVIEW_TEXT, voice)
    with open(cache_path, "wb") as f:
        f.write(wav_bytes)
    return wav_bytes


def _call_mimo_tts(text: str, voice: str = "冰糖", speed: float = 1.0) -> bytes:
    """Call MiMo TTS v2.5, return WAV bytes (base64 decoded)."""
    if not settings.MIMO_API_KEY or not settings.MIMO_API_KEY.startswith("sk-"):
        raise ValueError("MIMO_API_KEY not configured")

    if speed < 0.8:
        tone = "very slow and calm pace"
    elif speed < 1.0:
        tone = "slightly slow, gentle pace"
    elif speed > 1.3:
        tone = "fast and energetic pace"
    else:
        tone = "natural conversational pace"

    client = OpenAI(api_key=settings.MIMO_API_KEY, base_url=settings.MIMO_API_BASE)
    resp = client.chat.completions.create(
        model="mimo-v2.5-tts",
        messages=[
            {"role": "user", "content": f"{tone}, clear articulation, expressive tone"},
            {"role": "assistant", "content": text},
        ],
        audio={"format": "wav", "voice": voice},
    )
    audio_data = resp.choices[0].message.audio.data
    return base64.b64decode(audio_data)


def synthesize_full_script(
    lines: List[Dict],
    role_voice_map: Dict[int, str],
    output_dir: str,
    script_id: int,
    line_gap_ms: int = 0,
    progress_callback=None,
) -> Dict:
    """Synthesize all lines, splice into one WAV + SRT.

    Args:
        progress_callback: optional async callable(generated_count, total_count, failed_lines)

    Returns:
        {"audio_path": ..., "srt_path": ..., "failed_lines": [...]}
    """
    os.makedirs(output_dir, exist_ok=True)
    segments: List[AudioSegment] = []
    subtitles: List[pysrt.SubRipItem] = []
    failed_lines: List[int] = []
    current_ms = 0
    total = len(lines)

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
            seg = AudioSegment(audio_bytes, sample_width=2, frame_rate=24000, channels=1)
            seg = seg.strip_silence(silence_thresh=-50, silence_len=50, padding=20)
        except Exception as e:
            print(f"TTS failed line {line_no}: {e}")
            failed_lines.append(line_no)
            seg = AudioSegment.silent(duration=1000)

        segments.append(seg)
        dur_ms = len(seg)
        subtitles.append(pysrt.SubRipItem(
            index=line_no,
            start=pysrt.SubRipTime(milliseconds=current_ms),
            end=pysrt.SubRipTime(milliseconds=current_ms + dur_ms),
            text=text,
        ))
        current_ms += dur_ms + line_gap_ms

        # Report progress
        if progress_callback:
            progress_callback(i + 1, total, failed_lines)

    if not segments:
        raise ValueError("No audio segments generated")

    full = segments[0]
    gap = AudioSegment.silent(duration=line_gap_ms)
    for seg in segments[1:]:
        full = full + gap + seg

    audio_path = os.path.join(output_dir, f"script_{script_id}_full.wav")
    srt_path = os.path.join(output_dir, f"script_{script_id}_full.srt")
    full.export(audio_path, format="wav")
    pysrt.SubRipFile(items=subtitles).save(srt_path, encoding="utf-8")
    return {"audio_path": audio_path, "srt_path": srt_path, "failed_lines": failed_lines}
