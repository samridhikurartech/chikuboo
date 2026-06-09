from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


class StoryAgent:
    """Stage 1 local story provider with sample image fallbacks."""

    def __init__(self) -> None:
        self.sample_images_dir = Path("assets/sample_images")
        self.sample_images_dir.mkdir(parents=True, exist_ok=True)

    def get_story(self) -> dict[str, Any]:
        scenes = [
            {
                "scene_number": 1,
                "narration": "Chiku Rabbit was playing in the forest.",
                "image_path": "assets/sample_images/scene1.jpg",
            },
            {
                "scene_number": 2,
                "narration": "He found a bright carrot near a tiny path.",
                "image_path": "assets/sample_images/scene2.jpg",
            },
            {
                "scene_number": 3,
                "narration": "Chiku wanted to eat it, but he wondered who lost it.",
                "image_path": "assets/sample_images/scene3.jpg",
            },
            {
                "scene_number": 4,
                "narration": "Mini Squirrel came running and looked very worried.",
                "image_path": "assets/sample_images/scene4.jpg",
            },
            {
                "scene_number": 5,
                "narration": "Chiku smiled and gave the carrot back to Mini.",
                "image_path": "assets/sample_images/scene5.jpg",
            },
            {
                "scene_number": 6,
                "narration": "Everyone learned that honesty is the best policy.",
                "image_path": "assets/sample_images/scene6.jpg",
            },
        ]

        for scene in scenes:
            image_path = Path(scene["image_path"])
            if not image_path.exists():
                self._create_placeholder_image(image_path, scene["scene_number"])

        return {
            "title": "Chiku and the Lost Carrot",
            "moral": "Honesty is the best policy",
            "language": "English",
            "scenes": scenes,
        }

    def _create_placeholder_image(self, image_path: Path, scene_number: int) -> None:
        image_path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGB", (1080, 1920), "white")
        draw = ImageDraw.Draw(image)
        font = self._load_font(96)
        small_font = self._load_font(48)

        title = f"Scene {scene_number}"
        subtitle = "ChikuBoo Stage 1 Placeholder"
        title_box = draw.textbbox((0, 0), title, font=font)
        subtitle_box = draw.textbbox((0, 0), subtitle, font=small_font)

        draw.text(
            ((1080 - (title_box[2] - title_box[0])) // 2, 820),
            title,
            fill="black",
            font=font,
        )
        draw.text(
            ((1080 - (subtitle_box[2] - subtitle_box[0])) // 2, 950),
            subtitle,
            fill="gray",
            font=small_font,
        )
        image.save(image_path, quality=95)

    @staticmethod
    def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        for font_path in ["C:/Windows/Fonts/arialbd.ttf", "arialbd.ttf"]:
            try:
                return ImageFont.truetype(font_path, size)
            except OSError:
                continue
        return ImageFont.load_default()
