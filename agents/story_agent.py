from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from PIL import Image, ImageDraw, ImageFont


class StoryAgent:
    """Stage 2 Gemini story provider with placeholder image fallbacks."""

    def __init__(self) -> None:
        self.sample_images_dir = Path("assets/sample_images")
        self.sample_images_dir.mkdir(parents=True, exist_ok=True)

        load_dotenv()
        ##print("Current working directory:", os.getcwd())
        ##print("Gemini key:", os.getenv("GEMINI_API_KEY"))

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(api_key=api_key)

    def get_story(self) -> dict[str, Any]:

        prompt = """
Generate a YouTube Shorts children's story.

Main Character:
Chiku Rabbit

Character Appearance (MUST remain identical in every scene):

* Small white rabbit
* Blue overalls
* Red scarf
* Big expressive eyes
* Cute and friendly smile
* Pixar-style children's storybook character

Target Audience:
Children aged 3-8

Story Requirements:

* Total narration length: 80-120 words
* Exactly 6 scenes
* Each scene: 1-2 short sentences
* Fast-paced storytelling
* Simple vocabulary
* Positive emotional tone
* No violence
* No scary content
* No sadness
* No complex words

YouTube Shorts Structure:

Scene 1:
Strong hook that creates curiosity.

Scene 2:
Introduce a challenge or problem.

Scene 3:
Chiku attempts a solution.

Scene 4:
Unexpected but positive twist.

Scene 5:
Chiku succeeds or learns something.

Scene 6:
Clear moral lesson and happy ending.

Image Prompt Requirements:

For EVERY scene image_prompt include:

Character:

* Chiku Rabbit
* White rabbit
* Blue overalls
* Red scarf
* Big expressive eyes

Visual Style:

* Pixar-style 3D animation
* Bright vibrant colors
* Children's storybook illustration
* High detail
* Cute expressions
* Family friendly
* Vertical composition for YouTube Shorts
* Mobile-friendly framing
* Consistent character appearance

Return ONLY valid JSON.

JSON Format:

{
"title": "",
"moral": "",
"language": "English",
"scenes": [
{
"scene_number": 1,
"narration": "",
"image_prompt": ""
}
]
}

Do not return markdown.
Do not return explanations.
Do not wrap JSON in code blocks.
Return JSON only.
"""

        print("Generating story from Gemini...")

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        response_text = response.text.strip()

        # Remove markdown code fences if Gemini returns them
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "")
            response_text = response_text.strip()

        story = json.loads(response_text)

        for scene in story["scenes"]:
            scene["image_path"] = (
                f"assets/sample_images/scene{scene['scene_number']}.jpg"
            )

            image_path = Path(scene["image_path"])

            if not image_path.exists():
                self._create_placeholder_image(
                    image_path,
                    scene["scene_number"],
                )

        output_dir = Path("output/stories")
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(
            output_dir / "story.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                story,
                f,
                indent=2,
                ensure_ascii=False,
            )

        print("Story saved successfully")

        return story

    def _create_placeholder_image(
        self,
        image_path: Path,
        scene_number: int,
    ) -> None:
        image_path.parent.mkdir(parents=True, exist_ok=True)

        image = Image.new("RGB", (1080, 1920), "white")
        draw = ImageDraw.Draw(image)

        font = self._load_font(96)
        small_font = self._load_font(48)

        title = f"Scene {scene_number}"
        subtitle = "ChikuBoo Placeholder"

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
    def _load_font(
        size: int,
    ) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        for font_path in [
            "C:/Windows/Fonts/arialbd.ttf",
            "arialbd.ttf",
        ]:
            try:
                return ImageFont.truetype(font_path, size)
            except OSError:
                continue

        return ImageFont.load_default()