import os
import base64
import time
import requests
import cv2
import subprocess
from runwayml import RunwayML
from const import STORY_VIDEO_FOLDER, STORY_PROMPT_FOLDER, STORY_FRAME_FOLDER, RUNWAY_API_KEY
from utils import extract_last_frame, join_scenes_with_ffmpeg

# Initialize Runway client
runway_client = RunwayML(api_key=RUNWAY_API_KEY)

def animate_story(scene_list, input_image_path: str, model_name: str = "gen3a_turbo") -> str:
    """
    Animates a sequence of scenes using the RunwayML image-to-video API.

    Args:
        scene_list (list): List of scene dictionaries with 'id' and 'prompt'.
        input_image_path (str): Path to the cartoonized image used for prompting.
        model_name (str): RunwayML model to use. Default is "gen3a_turbo".

    Returns:
        str: Path to the final merged story video.
    """
    video_paths = []

    for i, scene in enumerate(scene_list):
        if isinstance(scene, dict):
            scene_id = scene.get("id", i + 1)
            prompt_text = scene.get("prompt", "")
        else:
            scene_id = i + 1
            prompt_text = scene
        prompt_path = os.path.join(STORY_PROMPT_FOLDER, f"{scene_id}.txt")

        if not prompt_text:
            with open(prompt_path) as f:
                prompt_text = f.read().strip()

        with open(input_image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")
            data_uri = f"data:image/png;base64,{base64_image}"

        print(f"Submitting scene {scene_id} to Runway...")
        task = runway_client.image_to_video.create(model=model_name, prompt_image=data_uri, prompt_text=prompt_text)
        task_id = task.id

        while True:
            time.sleep(10)
            task = runway_client.tasks.retrieve(task_id)
            print(f"Status for scene {scene_id}: {task.status}")
            if task.status in ["SUCCEEDED", "FAILED"]:
                break

        if task.status == "SUCCEEDED":
            if not task.output or not isinstance(task.output, list) or not task.output[0]:
                raise RuntimeError(f"RunwayML output for scene {scene_id} is empty or malformed: {task.output}")
            video_url = task.output[0]

            video_path = os.path.join(STORY_VIDEO_FOLDER, f"{scene_id}.mp4")
            video_data = requests.get(video_url).content
            with open(video_path, "wb") as f:
                f.write(video_data)
            print(f"Saved scene {scene_id} to: {video_path}")

            frame_path = os.path.join(STORY_FRAME_FOLDER, f"{scene_id}_last_frame.png")
            extract_last_frame(video_path, frame_path)
            input_image_path = frame_path  # use last frame as input for next
            video_paths.append(video_path)
        else:
            print(f"Failed to generate video for scene {scene_id}")
            break

    final_story_path = os.path.join(STORY_VIDEO_FOLDER, "final_story.mp4")
    join_scenes_with_ffmpeg(video_paths, final_story_path)
    return final_story_path