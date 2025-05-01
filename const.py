import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
You're writing a 3-part animated story based on this cartoon image: "{caption}".

Each scene must include:
1. One simple character movement — like walking, flying, jumping, or looking around.
2. One small background change — like light shifting, clouds moving, or wind blowing.
3. A minimal camera movement — such as a slow zoom, a slight pan to the left or right, or a gentle tilt. The movement should feel natural and not distract from the calm scene.

Format the response as a JSON list with 'id' and 'prompt'.
"""
