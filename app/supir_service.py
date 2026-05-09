from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageEnhance

# open uploaded image 
# apply simple restoration (upscaling + sharpening)
# save restored image to output directory
def mock_restore_image(input_path: Path, output_dir: Path, upscale: int = 2) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(input_path).convert("RGB")

    width, height = image.size
    new_size = (width * upscale, height * upscale)

    restored = image.resize(new_size, Image.Resampling.LANCZOS)

    sharpness = ImageEnhance.Sharpness(restored)
    restored = sharpness.enhance(1.5)

    contrast = ImageEnhance.Contrast(restored)
    restored = contrast.enhance(1.1)

    output_path = output_dir / f"{uuid4().hex}_restored.png"
    restored.save(output_path)

    return output_path