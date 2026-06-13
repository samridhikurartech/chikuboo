from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts

class VoiceAgent:
    """Stage 1 local narration provider."""

    def __init__(self) -> None:
        self.sample_audio_path = Path("assets/sample_audio/narration.mp3")
        self.sample_audio_path.parent.mkdir(parents=True, exist_ok=True)

    def get_narration_audio(
            self,
            story,
        ) -> Path:

            narration_text = " ".join(
                scene["narration"]
                for scene in story["scenes"]
            )
            
            print(
                "Generating narration from story..."
            )

            asyncio.run(
                self._generate_audio(
                    narration_text
                )
            )

            return self.sample_audio_path
        
        
    async def _generate_audio(
            self,
            text,
        ):

            communicate = edge_tts.Communicate(
                text,
                voice="en-US-AnaNeural",
                rate="-10%"
            )

            await communicate.save(
                str(self.sample_audio_path)
            )

            print(
                "Narration generated:",
                self.sample_audio_path
            )

    