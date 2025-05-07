import os
from typing import Optional
from PIL import Image
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from controlnet_aux import CannyDetector

from const import CARTOONIZED_FOLDER
from utils import crop_sides, get_device  

# Initialize the Canny edge detector once
canny = CannyDetector()

def create_pipeline(
    model_name: str,
    controlnet_name: str,
    device: torch.device
) -> StableDiffusionControlNetPipeline:
    """
    Initializes a Stable Diffusion pipeline with ControlNet support.

    Args:
        model_name (str): Base model identifier from Hugging Face.
        controlnet_name (str): ControlNet model identifier.
        device (torch.device): Device to run the model.

    Returns:
        StableDiffusionControlNetPipeline: Configured diffusion pipeline.
    """
    dtype = torch.float16 if device.type in ["cuda", "mps"] else torch.float32

    controlnet = ControlNetModel.from_pretrained(controlnet_name, torch_dtype=dtype)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        model_name,
        controlnet=controlnet,
        torch_dtype=dtype,
        safety_checker=None
    ).to(device)

    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    return pipe

def cartoonize_images(
    image_path: str,
    prompt: str,
    model_name: str = "lykon/dreamshaper-8",
    controlnet_name: str = "lllyasviel/sd-controlnet-canny",
    steps: int = 30,
    strength: float = 0.6,
    guidance_scale: float = 9.0,
    pipe: Optional[StableDiffusionControlNetPipeline] = None
) -> str:
    """
    Applies cartoonization to an input image using ControlNet + Stable Diffusion.

    Args:
        image_path (str): Path to the input image.
        prompt (str): Prompt describing the cartoon scene.
        model_name (str): Base model to use for generation.
        controlnet_name (str): ControlNet model to apply structural guidance.
        steps (int): Number of inference steps.
        strength (float): Denoising strength (0.0 - 1.0).
        guidance_scale (float): Prompt influence strength.
        pipe (Optional): Preloaded pipeline for reuse.

    Returns:
        str: File path to the saved cartoonized image.
    """
    os.makedirs(CARTOONIZED_FOLDER, exist_ok=True)
    device = get_device()

    # Only create a pipeline if not already provided
    if pipe is None:
        pipe = create_pipeline(model_name, controlnet_name, steps, strength, guidance_scale, device)

    try:
        input_image = Image.open(image_path).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Failed to open image: {image_path} — {e}")

    if input_image.width != input_image.height or input_image.width != 728:
        input_image = crop_sides(input_image, (728, 728))

    control_image = canny(input_image).resize(input_image.size)

    try:
        result = pipe(
            prompt=prompt,
            image=control_image,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            strength=strength
        ).images[0]

        image_name = os.path.basename(image_path)
        output_path = os.path.join(CARTOONIZED_FOLDER, f"cartoon_controlnet_dreamshaper_{image_name}")
        result.save(output_path)

    except Exception as e:
        raise RuntimeError(f"Cartoonization failed for {image_path}: {e}")

    return output_path
