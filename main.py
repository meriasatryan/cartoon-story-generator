import os
import argparse
from caption_generator import generate_cartoon_prompt, generate_story_prompt
from cartoonizer import cartoonize_images
from animator import animate_story
from const import PHOTOS_FOLDER


def main(cartoonize: bool = False) -> None:
    """
    Runs the end-to-end pipeline for cartoonizing and animating images from the photos folder.

    Steps:
    1. Generates a cartoon-style prompt from the image.
    2. Optionally cartoonizes the image using ControlNet + Stable Diffusion.
    3. Generates a 3-scene animated story prompt from the cartoon description.
    4. Calls the animation API to produce videos and joins them.

    Args:
        cartoonize (bool): If True, applies cartoonization before animation.
    """
    for filename in os.listdir(PHOTOS_FOLDER):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            image_path = os.path.join(PHOTOS_FOLDER, filename)
            print(f"\nProcessing image: {filename}")

            try:
                # Step 1: Caption + cartoon-style prompt
                cartoon_prompt = generate_cartoon_prompt(image_path)

                # Step 2: Optional cartoonization
                input_image_path = cartoonize_images(image_path, cartoon_prompt) if cartoonize else image_path

                # Step 3: Generate story scenes
                story_scenes = generate_story_prompt(cartoon_prompt)

                if not story_scenes:
                    raise ValueError("Story prompt generation returned empty results.")
                if not isinstance(story_scenes, list):
                    raise TypeError(f"Expected story_scenes to be a list, got {type(story_scenes)}")

                # Step 4: Animate and save result
                final_video_path = animate_story(story_scenes, input_image_path)
                print(f"Saved video: {final_video_path}")

            except Exception as e:
                print(f"Error while processing {filename}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cartoon + Animation Pipeline")
    parser.add_argument(
        "--cartoonize",
        action="store_true",
        help="Cartoonize images before animation."
    )
    args = parser.parse_args()
    main(cartoonize=args.cartoonize)
