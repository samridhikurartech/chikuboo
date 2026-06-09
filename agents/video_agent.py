from __future__ import annotations

from pathlib import Path
from typing import Any

from moviepy import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    ImageClip,
    concatenate_videoclips,
)


class VideoAgent:
    """Creates the Stage 1 vertical video using local assets only."""

    def __init__(self) -> None:
        self.video_width = 1080
        self.video_height = 1920
        self.output_path = Path("output/videos/chikuboo_episode_001.mp4")
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def create_video(
        self,
        story: dict[str, Any],
        narration_audio_path: Path,
    ) -> Path:
        scenes = story["scenes"]

        audio = AudioFileClip(str(narration_audio_path))
        scene_duration = audio.duration / len(scenes)

        clips = [
            self._create_scene_clip(
                Path(scene["image_path"]),
                scene_duration,
            )
            for scene in scenes
        ]

        video = concatenate_videoclips(clips, method="compose")
        video = video.with_audio(audio)
        video = video.with_duration(audio.duration)

        video.write_videofile(
            str(self.output_path),
            fps=30,
            codec="libx264",
            audio_codec="aac",
        )

        audio.close()
        video.close()

        for clip in clips:
            clip.close()

        return self.output_path

    def _create_scene_clip(
        self,
        image_path: Path,
        duration: float,
    ) -> CompositeVideoClip:

        background = ColorClip(
            size=(self.video_width, self.video_height),
            color=(255, 255, 255),
            duration=duration,
        )

        image = (
            ImageClip(str(image_path))
            .with_duration(duration)
            .resized(height=self.video_height)
            .with_position("center")
        )

        return CompositeVideoClip(
            [background, image],
            size=(self.video_width, self.video_height),
        )