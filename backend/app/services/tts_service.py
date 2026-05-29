"""TTS service — MiMo (Xiaomi) TTS v2.5 via OpenAI SDK.

Groups lines by voice and synthesizes each voice group in one API call.
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


def _cache_path(text: str, voice: str) -> str:
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


def _call_mimo_tts(text: str, voice: str = "冰糖", speed: float = 1.0) -> bytes:
    """Call MiMo TTS v2.5, return WAV bytes. Caches at default speed."""
    if not settings.MIMO_API_KEY or not settings.MIMO_API_KEY.startswith("sk-"):
        raise ValueError("MIMO_API_KEY not configured")

    if speed == 1.0:
        cp = _cache_path(text, voice)
        if os.path.exists(cp):
            with open(cp, "rb") as f:
                return f.read()

    tone = _speed_tone(speed)
    client = OpenAI(api_key=settings.MIMO_API_KEY, base_url=settings.MIMO_API_BASE)
    resp = client.chat.completions.create(
        model="mimo-v2.5-tts",
        messages=[
            {"role": "user", "content": f"{tone}, clear articulation, expressive tone, natural pacing"},
            {"role": "assistant", "content": text},
        ],
        audio={"format": "wav", "voice": voice},
    )
    wav = base64.b64decode(resp.choices[0].message.audio.data)
    if speed == 1.0:
        with open(_cache_path(text, voice), "wb") as f:
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


def synthesize_full_script(
    lines: List[Dict],
    role_voice_map: Dict[int, str],
    output_dir: str,
    script_id: int,
    line_gap_ms: int = 300,
    progress_callback: Optional[Callable] = None,
) -> Dict:
    """Synthesize all lines grouped by voice, splice into one WAV + SRT.

    Groups lines with the same voice into one MiMo API call, then estimates
    per-line timestamps proportionally by character count.
    """
    os.makedirs(output_dir, exist_ok=True)
    total = len(lines)

    # ── Group lines by voice ─────────────────────────────────────
    groups: Dict[str, List[Dict]] = {}
    order: List[str] = []
    for ln in lines:
        voice = role_voice_map.get(ln.get("role_id"), "冰糖")
        if voice not in groups:
            groups[voice] = []
            order.append(voice)
        groups[voice].append(ln)

    # ── Synthesize each voice group as one batch ──────────────────
    voice_segments: Dict[str, AudioSegment] = {}
    failed_lines: List[int] = []
    done = 0

    for voice in order:
        glines = groups[voice]
        # Join lines with newlines, preserve per-line info for subtitle
        combined_text = "\n".join(str(ln.get("content", "")).strip() for ln in glines)
        try:
            audio_bytes = _call_mimo_tts(combined_text, voice)
            seg = AudioSegment(audio_bytes, sample_width=2, frame_rate=24000, channels=1)
            voice_segments[voice] = seg.strip_silence(silence_thresh=-50, silence_len=50, padding=20)
        except Exception as e:
            print(f"TTS batch failed for voice {voice}: {e}")
            for ln in glines:
                failed_lines.append(ln.get("line_number", 0))
            voice_segments[voice] = AudioSegment.silent(duration=len(glines) * 1000)

        done += len(glines)
        if progress_callback:
            progress_callback(done, total, failed_lines)

    # ── Build subtitle timestamps proportionally ──────────────────
    subtitles: List[pysrt.SubRipItem] = []
    current_ms = 0

    for line in lines:
        voice = role_voice_map.get(line.get("role_id"), "冰糖")
        seg = voice_segments.get(voice)
        if not seg:
            continue

        # Find this line's position in its voice group
        glines = groups[voice]
        total_chars = sum(len(str(l.get("content", ""))) for l in glines) or 1
        text = str(line.get("content", "")).strip()
        line_chars = len(text)
        dur_ratio = line_chars / total_chars
        seg_total_ms = len(seg)
        line_dur_ms = int(dur_ratio * seg_total_ms)

        subtitles.append(pysrt.SubRipItem(
            index=line.get("line_number", 1),
            start=pysrt.SubRipTime(milliseconds=current_ms),
            end=pysrt.SubRipTime(milliseconds=current_ms + line_dur_ms),
            text=text,
        ))
        current_ms += line_dur_ms
        # Add gap between same-voice lines (but MiMo already handles pacing internally,
        # so we only add gap between different-voice groups)

    # ── Splice all voice segments in order ────────────────────────
    full = voice_segments[order[0]]
    base_frame_rate = full.frame_rate
    for v in order[1:]:
        if line_gap_ms > 0:
            gap = AudioSegment.silent(duration=line_gap_ms, frame_rate=base_frame_rate)
            full = full + gap
        full = full + voice_segments[v]

    audio_path = os.path.join(output_dir, f"script_{script_id}_full.wav")
    srt_path = os.path.join(output_dir, f"script_{script_id}_full.srt")
    full.export(audio_path, format="wav")
    pysrt.SubRipFile(items=subtitles).save(srt_path, encoding="utf-8")
    return {"audio_path": audio_path, "srt_path": srt_path, "failed_lines": failed_lines}
