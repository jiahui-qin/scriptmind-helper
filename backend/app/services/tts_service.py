"""TTS service — MiMo (Xiaomi) TTS v2.5 via OpenAI SDK.

Ref: https://platform.xiaomimimo.com/docs/zh-CN/usage-guide/speech-synthesis-v2.5
"""
import os
import base64
from typing import List, Dict
from openai import OpenAI
from pydub import AudioSegment
import pysrt
from app.config import settings

# Supported MiMo TTS voices
MIMO_VOICES = ["mimo_default", "冰糖", "茉莉", "苏打", "白桦", "Mia", "Chloe", "Milo", "Dean"]


def _call_mimo_tts(text: str, voice: str = "Chloe", speed: float = 1.0) -> bytes:
    """Call MiMo TTS v2.5, return WAV bytes (base64 decoded).

    Uses the speech-synthesis-v2.5 format: messages with user/assistant roles,
    audio dict with format and voice.
    """
    if not settings.MIMO_API_KEY or not settings.MIMO_API_KEY.startswith("sk-"):
        raise ValueError("MIMO_API_KEY not configured")

    # Speed → tone instruction mapping
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
) -> Dict[str, str]:
    """Synthesize all lines, splice into one WAV + SRT."""
    os.makedirs(output_dir, exist_ok=True)
    segments = []
    subtitles = []
    current_ms = 0

    for ln in lines:
        role_id = ln.get("role_id")
        voice = role_voice_map.get(role_id, "Chloe")
        speed = ln.get("speech_rate", 1.0)
        text = str(ln.get("content", "")).strip()
        if not text:
            continue
        try:
            audio_bytes = _call_mimo_tts(text, voice, speed)
            # MiMo returns 24kHz mono WAV
            seg = AudioSegment(audio_bytes, sample_width=2, frame_rate=24000, channels=1)
        except Exception as e:
            print(f"TTS failed line {ln.get('line_number')}: {e}")
            seg = AudioSegment.silent(duration=1000)

        segments.append(seg)
        dur_ms = len(seg)
        subtitles.append(pysrt.SubRipItem(
            index=ln.get("line_number", 1),
            start=pysrt.SubRipTime(milliseconds=current_ms),
            end=pysrt.SubRipTime(milliseconds=current_ms + dur_ms),
            text=text,
        ))
        current_ms += dur_ms + 300

    if not segments:
        raise ValueError("No audio segments generated")

    full = segments[0]
    silence = AudioSegment.silent(duration=300)
    for seg in segments[1:]:
        full = full + silence + seg

    audio_path = os.path.join(output_dir, f"script_{script_id}_full.wav")
    srt_path = os.path.join(output_dir, f"script_{script_id}_full.srt")
    full.export(audio_path, format="wav")
    pysrt.SubRipFile(items=subtitles).save(srt_path, encoding="utf-8")
    return {"audio_path": audio_path, "srt_path": srt_path}
