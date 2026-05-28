"""TTS service — call MiMo (Xiaomi) TTS API via OpenAI SDK, splice audio, generate SRT."""
import os
import base64
from typing import List, Dict
from openai import OpenAI
from pydub import AudioSegment
import pysrt
from app.config import settings


MIMO_VOICES = ["Chloe", "James", "Emma", "William", "Ava", "Michael", "Sophia", "Daniel", "Mia"]


def get_available_voices() -> List[str]:
    return MIMO_VOICES


def _call_mimo_tts(text: str, voice: str = "Chloe", speed: float = 1.0) -> bytes:
    """Call MiMo TTS v2.5 via OpenAI SDK, return WAV bytes."""
    if not settings.MIMO_API_KEY:
        raise ValueError("MIMO_API_KEY not configured")

    speed_instruction = "normal pace"
    if speed < 0.8:
        speed_instruction = "very slow pace"
    elif speed < 1.0:
        speed_instruction = "slightly slow pace"
    elif speed > 1.3:
        speed_instruction = "fast pace"

    client = OpenAI(api_key=settings.MIMO_API_KEY, base_url=settings.MIMO_API_BASE)
    resp = client.chat.completions.create(
        model=settings.MIMO_TTS_MODEL,
        messages=[
            {"role": "user", "content": f"{speed_instruction}, clear articulation"},
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
    """Synthesize full script into one WAV + SRT subtitle."""
    os.makedirs(output_dir, exist_ok=True)
    audio_segments = []
    subtitles = []
    silence = AudioSegment.silent(duration=500)

    for ln in lines:
        role_id = ln.get("role_id")
        voice = role_voice_map.get(role_id, "Chloe")
        speed = ln.get("speech_rate", 1.0)
        text = ln.get("content", "").strip()
        if not text:
            continue
        try:
            audio_bytes = _call_mimo_tts(text, voice, speed)
            seg = AudioSegment(audio_bytes, sample_width=2, frame_rate=24000, channels=1)
        except Exception as e:
            print(f"TTS failed for line {ln.get('line_number')}: {e}")
            seg = AudioSegment.silent(duration=1000)
        audio_segments.append(seg)
        audio_segments.append(silence)
        start_ms = sum(len(s) for s in audio_segments[:-1])
        end_ms = start_ms + len(seg)
        item = pysrt.SubRipItem(
            index=ln["line_number"],
            start=pysrt.SubRipTime(milliseconds=start_ms),
            end=pysrt.SubRipTime(milliseconds=end_ms),
            text=text,
        )
        subtitles.append(item)

    if not audio_segments:
        raise ValueError("No audio segments generated")
    full_audio = audio_segments[0]
    for seg in audio_segments[1:]:
        full_audio += seg

    audio_path = os.path.join(output_dir, f"script_{script_id}_full.wav")
    srt_path = os.path.join(output_dir, f"script_{script_id}_full.srt")
    full_audio.export(audio_path, format="wav")
    pysrt.SubRipFile(items=subtitles).save(srt_path, encoding="utf-8")
    return {"audio_path": audio_path, "srt_path": srt_path}
