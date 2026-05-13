from pathlib import Path
from uuid import uuid4

import cv2
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

        # 1. Light denoising
        denoised = cv2.fastNlMeansDenoisingColored(
            image,
            None,
            h=4,
            hColor=4,
            templateWindowSize=7,
            searchWindowSize=21,
        )

        # 2. High-quality upscale
        height, width = denoised.shape[:2]

        upscaled = cv2.resize(
            denoised,
            (width * upscale, height * upscale),
            interpolation=cv2.INTER_LANCZOS4,
        )

        # 3. Local contrast enhancement
        lab = cv2.cvtColor(upscaled, cv2.COLOR_BGR2LAB)

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8),
        )

        l = clahe.apply(l)

        merged = cv2.merge((l, a, b))

        contrast = cv2.cvtColor(
            merged,
            cv2.COLOR_LAB2BGR,
        )

        # 4. Sharpening
        blur = cv2.GaussianBlur(
            contrast,
            (0, 0),
            sigmaX=1.2,
        )

        sharpened = cv2.addWeighted(
            contrast,
            1.8,
            blur,
            -0.8,
            0,
        )
        # 5. Final PIL enhancement
        rgb = cv2.cvtColor(
            sharpened,
            cv2.COLOR_BGR2RGB,
        )

        pil_img = Image.fromarray(rgb)

        pil_img = ImageEnhance.Contrast(
            pil_img
        ).enhance(1.15)

        pil_img = ImageEnhance.Sharpness(
            pil_img
        ).enhance(1.6)

        pil_img = ImageEnhance.Color(
            pil_img
        ).enhance(1.08)

        
        # Save result
        output_path = (
            output_dir
            / f"{uuid4().hex}_restored.png"
        )

        pil_img.save(output_path)

        return output_path


supir_service = SUPIRService()