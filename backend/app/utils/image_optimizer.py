import os
from PIL import Image
from flask import current_app


def optimize_image(file_path, output_path=None, quality=75, max_size=None):
    """
    Optimizes and compresses an image file.

    Args:
        file_path (str): Absolute path to the input image.
        output_path (str): Where to save optimized image. Defaults to overwriting original.
        quality (int): JPEG/WebP quality (1–100). Default is 75.
        max_size (tuple): Optional (width, height) max dimensions.

    Returns:
        str: Final saved path of optimized image.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image not found at: {file_path}")

    try:
        with Image.open(file_path) as img:
            img_format = img.format  # Preserve original format

            if max_size:
                img.thumbnail(max_size, Image.ANTIALIAS)

            # Default output to same file path (overwrite)
            output_path = output_path or file_path

            # Save optimized
            if img_format.upper() in ['JPEG', 'JPG']:
                img.save(output_path, format='JPEG', quality=quality, optimize=True)
            elif img_format.upper() == 'PNG':
                img.save(output_path, format='PNG', optimize=True)
            else:
                # Convert unsupported formats to JPEG
                output_path = os.path.splitext(output_path)[0] + ".jpg"
                rgb_img = img.convert("RGB")
                rgb_img.save(output_path, format='JPEG', quality=quality, optimize=True)

            return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to optimize image: {str(e)}")
