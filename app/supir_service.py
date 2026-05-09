from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageEnhance


class SUPIRService:
    def __init__(self):
        self.model_loaded = False

    def load_model(self):
        """
        Mock model loading
        """

        print("Loading SUPIR model...")

        self.model_loaded = True

        print("SUPIR model loaded.")

    def restore_image(
        self,
        input_path: Path,
        output_dir: Path,
        upscale: int = 2,
    ) -> Path:

        if not self.model_loaded:
            self.load_model()

        output_dir.mkdir(parents=True, exist_ok=True)

        image = Image.open(input_path).convert("RGB")

        width, height = image.size

        new_size = (
            width * upscale,
            height * upscale,
        )

        restored = image.resize(
            new_size,
            Image.Resampling.LANCZOS,
        )

        sharpness = ImageEnhance.Sharpness(restored)

        restored = sharpness.enhance(1.5)

        contrast = ImageEnhance.Contrast(restored)

        restored = contrast.enhance(1.1)

        output_path = (
            output_dir /
            f"{uuid4().hex}_restored.png"
        )

        restored.save(output_path)

        return output_path


supir_service = SUPIRService()