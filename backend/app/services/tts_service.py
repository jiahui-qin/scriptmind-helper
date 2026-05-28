"""TTS service — call Moonshot TTS API, splice audio, generate SRT."""
import os
import json
import requests
from typing import List, Dict, Optional
from pydub import AudioSegment
import pysrt

from app.config import settings


def _call_moonshot_tts(text: str, voice: str, speed: float = 1.0) -> bytes:
    """Call Moonshot TTS v2.5 Native API, return audio bytes (WAV)."""
    if not settings.MOONSHOT_API_KEY:
        raise ValueError("MOONSHOT_API_KEY not configured")
    headers = {
        "Authorization": f"Bearer {settings.MOONSHOT_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "moonshot-v1-audio",
        "input": text,
        "voice": voice,
        "response_format": "wav",
        "speed": speed,
    }
    resp = requests.post(
        settings.MOONSHOT_TTS_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    # Moonshot TTS returns raw audio bytes
    return resp.content


def synthesize_full_script(
    lines: List[Dict],
    role_voice_map: Dict[int, str],
    output_dir: str,
    script_id: int,
) -> Dict[str, str]:
    """Synthesize full script into one WAV file + SRT subtitle.
    
    Args:
        lines: List of {id, line_number, content, role_id, emotion_tag, speech_rate}
        role_voice_map: {role_id: voice_name}
        output_dir: where to save output files
        script_id: for naming output files
    
    Returns: {audio_path, srt_path}
    """
    os.makedirs(output_dir, exist_ok=True)

    audio_segments: List[AudioSegment] = []
    subtitles: List[pysrt.SubRipItem] = []

    # Silence between lines (500ms)
    silence = AudioSegment.silent(duration=500)

    for ln in lines:
        role_id = ln.get('role_id')
        voice = role_voice_map.get(role_id, 'female-qn-qingse')
        speed = ln.get('speech_rate', 1.0)
        text = ln.get('content', '').strip()
        if not text:
            continue

        try:
            audio_bytes = _call_moonshot_tts(text, voice, speed)
            seg = AudioSegment.from_file(audio_bytes, format='wav')
        except Exception as e:
            print(f"TTS failed for line {ln.get('line_number')}: {e}")
            # Generate silence as placeholder
            seg = AudioSegment.silent(duration=1000)

        audio_segments.append(seg)
        audio_segments.append(silence)

        # Build SRT entry
        start_ms = sum(len(s) for s in audio_segments[:-1])
        end_ms = start_ms + len(seg)
        item = pysrt.SubRipItem(
            index=ln['line_number'],
            start=pysrt.SubRipTime(milliseconds=start_ms),
            end=pysrt.SubRipTime(milliseconds=end_ms),
            text=text,
        )
        subtitles.append(item)

    # Concatenate all audio
    if not audio_segments:
        raise ValueError("No audio segments generated")
    full_audio = audio_segments[0]
    for seg in audio_segments[1:]:
        full_audio += seg

    audio_path = os.path.join(output_dir, f"script_{script_id}_full.wav")
    srt_path = os.path.join(output_dir, f"script_{script_id}_full.srt")

    full_audio.export(audio_path, format='wav')
    subs = pysrt.SubRipFile(items=subtitles)
    subs.save(srt_path, encoding='utf-8')

    return {'audio_path': audio_path, 'srt_path': srt_path}
