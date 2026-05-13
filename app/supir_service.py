from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np
from PIL import Image, ImageEnhance


class SUPIRService:
    def __init__(self):
        self.model_loaded = False

    def load_model(self):
        print("Lightweight SUPIR-inspired restoration pipeline is ready.")
        self.model_loaded = True

    def restore_image(
        self,
        input_path: Path,
        output_dir: Path,
        upscale: int = 2,
        mode: str = "lightweight",
        model_type: str = "Q",
    ) -> Path:
        if not self.model_loaded:
            self.load_model()

        output_dir.mkdir(parents=True, exist_ok=True)

        image = cv2.imread(str(input_path))
        if image is None:
            raise ValueError("Could not read uploaded image.")

        # 1. Denoise
        denoised = cv2.fastNlMeansDenoisingColored(
            image,
            None,
            h=7,
            hColor=7,
            templateWindowSize=7,
            searchWindowSize=21,
        )

        # 2. Upscale
        height, width = denoised.shape[:2]
        upscaled = cv2.resize(
            denoised,
            (width * upscale, height * upscale),
            interpolation=cv2.INTER_CUBIC,
        )

        # 3. Sharpen
        blur = cv2.GaussianBlur(upscaled, (0, 0), sigmaX=1.0)
        sharpened = cv2.addWeighted(upscaled, 1.5, blur, -0.5, 0)

        # 4. Slight contrast improvement with PIL
        rgb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        pil_img = ImageEnhance.Contrast(pil_img).enhance(1.08)
        pil_img = ImageEnhance.Sharpness(pil_img).enhance(1.25)

        output_path = output_dir / f"{uuid4().hex}_restored.png"
        pil_img.save(output_path)

        return output_path


supir_service = SUPIRService()