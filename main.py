from __future__ import annotations

from PIL import Image

if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

import logging
import sys

from agents.story_agent import StoryAgent
from agents.video_agent import VideoAgent
from agents.voice_agent import VoiceAgent
from agents.image_agent import ImageAgent


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> int:
    setup_logging()
    logger = logging.getLogger("chikuboo")

    try:
        logger.info("Step 1/4: Loading hardcoded story")
        story = StoryAgent().get_story()
        logger.info("Story loaded: %s", story["title"])

        logger.info("Step 2/5: Generating images")
        ImageAgent().generate_images(story)

        logger.info("Step 3/5: Loading sample narration audio")
        audio_path = VoiceAgent().get_narration_audio()

        logger.info("Step 4/5: Rendering video")
        video_path = VideoAgent().create_video(story, audio_path)

        logger.info("Step 5/5: Done")
        return 0
    except Exception:
        logger.exception("Pipeline failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
