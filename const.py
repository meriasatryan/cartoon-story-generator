import os

# === API KEYS ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")

# === BASE DIRECTORIES ===
BASE_DIR = os.path.join(os.path.dirname(__file__), "data")

PHOTOS_FOLDER = os.path.join(BASE_DIR, "photos")
PROMPT_FOLDER = os.path.join(BASE_DIR, "prompts")
CARTOONIZED_FOLDER = os.path.join(BASE_DIR, "cartoonized_images")
STORY_PROMPT_FOLDER = os.path.join(BASE_DIR, "story_prompts")

# === OUTPUT FOLDERS ===
STORY_FOLDER = os.path.join(BASE_DIR, "stories")
STORY_VIDEO_FOLDER = os.path.join(STORY_FOLDER, "videos")
STORY_FRAME_FOLDER = os.path.join(STORY_FOLDER, "frames")

# Ensure output folders exist
os.makedirs(STORY_PROMPT_FOLDER, exist_ok=True)
os.makedirs(STORY_VIDEO_FOLDER, exist_ok=True)
os.makedirs(STORY_FRAME_FOLDER, exist_ok=True)

# === PROMPT TEMPLATES ===

# Template for generating cartoon-style prompts from image captions
CARTOON_INSTRUCTION_TEMPLATE = """
Turn this image description into a simple prompt for a cartoon-style illustration.
It should describe the main object, background, and lighting in one sentence.

Example output:
"A cartoon-style illustration of a penguin standing on rocks by the water, with snowy mountains in the background and soft, natural lighting."

Image description: "{caption}"
"""

# Template for generating a 3-part animated story from the cartoon caption
STORY_INSTRUCTION_TEMPLATE = """
You're writing three independent animation scene prompts based on the cartoon image: "{caption}".

Each prompt must:
- Be calm, grounded, and simple.
- Include one clear character action (e.g., walking, jumping, turning head).
- Include one small environmental change (e.g., snow falling, wind blowing, clouds drifting).
- Include one camera movement (e.g., slow zoom, gentle pan, upward tilt).
- Avoid any reference to sequence or order (do not say "first", "next", or "finally").
- Be no longer than 1–2 sentences.

Format the result as a JSON list where each object has an "id" and a "prompt" field.

Example output:
[
  {{
    "id": 1,
    "prompt": "The penguin turns its head to the side as a gentle wind brushes across the snow and the camera softly pans left."
  }},
  {{
    "id": 2,
    "prompt": "The penguin walks forward slowly while a few snowflakes begin to fall and the camera zooms in slightly."
  }},
  {{
    "id": 3,
    "prompt": "The penguin pauses near a rock as a faint light glows behind the mountains and the camera tilts upward."
  }}
]
"""
