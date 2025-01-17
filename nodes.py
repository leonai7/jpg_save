from nodes import SaveImage
import json
from PIL import Image
import numpy as np
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args # type: ignore
import folder_paths # type: ignore
from folder_paths import get_filename_list # type: ignore
import comfy
import os

from PIL import Image
import os
import numpy as np

class SaveImageJPGNoMeta(SaveImage):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Input image
                "filename": ("STRING", {"default": "image.jpg"}),  # Input for filename
                "quality": ("INT", {"default": 92, "min": 1, "max": 100, "step": 1}),  # Quality slider
            },
        }

    CATEGORY = "_JPG - LAI"
    RETURN_TYPES = ()
    FUNCTION = "save_image"

    def save_image(self, images, filename="image.jpg", quality=92):
        # Convert image tensor to numpy array and then to PIL Image
        img = Image.fromarray(np.clip(255.0 * images[0].cpu().numpy(), 0, 255).astype(np.uint8))
        
        # Ensure the filename has the correct extension
        if not filename.lower().endswith(".jpg"):
            filename = f"{filename}.jpg"
        
        # Save the image with the provided filename and quality
        file_path = os.path.join(self.output_dir, filename)
        img.save(file_path, "JPEG", quality=quality, optimize=True)
        
        return {"ui": {"images": [{"filename": filename}]}}
        
# Export node
NODE_CLASS_MAPPINGS = {
    "SaveImageJPGNoMeta": SaveImageJPGNoMeta,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageJPGNoMeta": "Save Image JPG No Meta",
}
