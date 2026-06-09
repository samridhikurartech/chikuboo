from __future__ import annotations

import wave
from pathlib import Path


class VoiceAgent:
    """Stage 1 local narration provider."""

    def __init__(self) -> None:
        self.sample_audio_path = Path("assets/sample_audio/narration.wav")
        self.sample_audio_path.parent.mkdir(parents=True, exist_ok=True)

    def get_narration_audio(self) -> Path:
        if not self.sample_audio_path.exists():
            self._create_silent_audio(self.sample_audio_path)

        return self.sample_audio_path

    @staticmethod
    def _create_silent_audio(audio_path: Path) -> None:
        audio_path.parent.mkdir(parents=True, exist_ok=True)

        duration_seconds = 36
        sample_rate = 44100

        with wave.open(str(audio_path), "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            silence = b"\x00\x00" * sample_rate * duration_seconds
            wav_file.writeframes(silence)

        print(f"Created silent audio: {audio_path}")