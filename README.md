# ChikuBoo Stage 1 MVP

This stage validates the local video pipeline only.

No external services are used:

- No OpenAI
- No Gemini
- No Puter
- No ElevenLabs
- No API keys
- No internet required

Running:

```powershell
python main.py
```

generates:

```text
output/videos/chikuboo_episode_001.mp4
```

## Project Structure

```text
chikuboo/
├── main.py
├── agents/
│   ├── story_agent.py
│   ├── voice_agent.py
│   └── video_agent.py
├── assets/
│   ├── sample_images/
│   └── sample_audio/
├── output/
│   └── videos/
└── requirements.txt
```

## How It Works

1. `StoryAgent` returns a hardcoded 6-scene story.
2. If sample scene images are missing, it creates simple Pillow placeholder images.
3. `VoiceAgent` loads `assets/sample_audio/narration.mp3`.
4. If narration audio is missing, it creates a short silent MP3.
5. `VideoAgent` renders a vertical 1080x1920 video using MoviePy.

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

Final file:

```text
output/videos/chikuboo_episode_001.mp4
```
