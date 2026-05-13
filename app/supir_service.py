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
        mode = mode.lower()
        # 3 restoration model 
        # balanced - default, good for most images
        # strong - strong denoise, bigger contrast, sharpening
        # old photo - gray scale ? contrast boost 
        if mode == "strong":
            denoise_h = 8
            clahe_clip = 3.0
            sharpen_amount = 2.1
            blur_weight = -1.1
            contrast_boost = 1.22
            sharpness_boost = 1.9
            color_boost = 1.12

        elif mode == "old_photo":
            denoise_h = 6
            clahe_clip = 3.5
            sharpen_amount = 2.0
            blur_weight = -1.0
            contrast_boost = 1.28
            sharpness_boost = 2.0
            color_boost = 0.95

        else:
            denoise_h = 4
            clahe_clip = 2.0
            sharpen_amount = 1.7
            blur_weight = -0.7
            contrast_boost = 1.15
            sharpness_boost = 1.5
            color_boost = 1.06

        denoised = cv2.fastNlMeansDenoisingColored(
            image,
            None,
            h=denoise_h,
            hColor=denoise_h,
            templateWindowSize=7,
            searchWindowSize=21,
        )

        height, width = denoised.shape[:2]
        upscaled = cv2.resize(
            denoised,
            (width * upscale, height * upscale),
            interpolation=cv2.INTER_LANCZOS4,
        )

        if mode == "old_photo":
            gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)
            upscaled = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        lab = cv2.cvtColor(upscaled, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=clahe_clip,
            tileGridSize=(8, 8),
        )

        l = clahe.apply(l)
        merged = cv2.merge((l, a, b))
        contrast = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

        smooth = cv2.bilateralFilter(
            contrast,
            d=5,
            sigmaColor=50,
            sigmaSpace=50,
        )

        blur = cv2.GaussianBlur(
            smooth,
            (0, 0),
            sigmaX=1.0,
        )

        sharpened = cv2.addWeighted(
            smooth,
            sharpen_amount,
            blur,
            blur_weight,
            0,
        )

        rgb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

        pil_img = ImageEnhance.Contrast(pil_img).enhance(contrast_boost)
        pil_img = ImageEnhance.Sharpness(pil_img).enhance(sharpness_boost)
        pil_img = ImageEnhance.Color(pil_img).enhance(color_boost)

        output_path = output_dir / f"{uuid4().hex}_{mode}_restored.png"
        pil_img.save(output_path)

        return output_path


supir_service = SUPIRService()