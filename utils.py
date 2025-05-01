import os
import cv2
import subprocess
import tempfile
from typing import List
from PIL import Image
import imageio_ffmpeg


def crop_sides(image: Image.Image, target_size: tuple = (728, 728)) -> Image.Image:
    """
    Resize and crop the sides of an image to match a target size.

    Args:
        image (Image.Image): Input image to crop.
        target_size (tuple): Desired output size (width, height).

    Returns:
        Image.Image: Cropped and resized image.
    """
    width, height = image.size
    target_width, target_height = target_size
    new_height = target_height
    new_width = int((new_height / height) * width)
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - target_width) // 2 - 10
    right = left + target_width + 20

    return image.crop((max(0, left), 0, min(new_width, right), new_height))


def extract_last_frame(video_path: str, output_path: str) -> None:
    """
    Extract the last frame from a video and save it as an image.

    Args:
        video_path (str): Path to the video file.
        output_path (str): Path to save the last frame image.
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
    cap.release()


def join_scenes_with_ffmpeg(video_paths: List[str], output_path: str) -> None:
    """
    Merge multiple video clips into a single video using ffmpeg.

    Args:
        video_paths (List[str]): List of paths to video files.
        output_path (str): Path to save the combined video.
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as list_file:
        for path in video_paths:
            if os.path.exists(path):
                list_file.write(f"file '{os.path.abspath(path)}'\n")
        temp_list_path = list_file.name

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    command = [
        ffmpeg_exe,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_list_path,
        "-c", "copy",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed to join video scenes: {e}")
    finally:
        os.remove(temp_list_path)
