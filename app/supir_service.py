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
        mode: str = "balanced",
        model_type: str = "Q",
    ) -> Path:

        if not self.model_loaded:
            self.load_model()

        output_dir.mkdir(parents=True, exist_ok=True)

        image = cv2.imread(str(input_path))

        if image is None:
            raise ValueError("Could not read uploaded image.")
        mode = mode.lower()
        
        model_type = model_type.upper()

        if model_type == "Q":
            contrast_multiplier = 1.12
            sharpness_multiplier = 1.15
            denoise_multiplier = 1.0
        else:
            contrast_multiplier = 1.0
            sharpness_multiplier = 0.9
            denoise_multiplier = 1.25
            
        # 3 restoration model 
        # balanced - default, good for most images
        # strong - strong denoise, bigger contrast, sharpening
        # old photo - gray scale ? contrast boost 
        if mode == "strong":
            #denoise_h = 8
            denoise_h = int(7 * denoise_multiplier)
            clahe_clip = 2.6
            sharpen_amount = 1.75
            blur_weight = -0.75
            #contrast_boost = 1.22
            #sharpness_boost = 1.9
            contrast_boost = 1.16 * contrast_multiplier
            sharpness_boost = 1.45 * sharpness_multiplier
            color_boost = 1.08

        elif mode == "old_photo":
            #denoise_h = 6
            denoise_h = int(6 * denoise_multiplier)
            clahe_clip = 2.3
            sharpen_amount = 1.45
            blur_weight = -1.45
            #contrast_boost = 1.28
            contrast_boost = 1.12 * contrast_multiplier
            #sharpness_boost = 2.0
            sharpness_boost = 1.25 * sharpness_multiplier
            color_boost = 0.85

        else:
            denoise_h = int(4 * denoise_multiplier)
            clahe_clip = 1.8
            sharpen_amount = 1.45
            blur_weight = -0.45
            contrast_boost = 1.08 * contrast_multiplier
            sharpness_boost = 1.20 * sharpness_multiplier
            color_boost = 1.04

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
            sigmaColor=45,
            sigmaSpace=45,
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

        if mode == "old_photo":
            grayscale = pil_img.convert("L")
            pil_img = Image.merge(
                "RGB",
                (
                    grayscale,
                    grayscale,
                    grayscale,
                ),
            )

            pil_img = ImageEnhance.Contrast(pil_img).enhance(1.08)
            pil_img = ImageEnhance.Sharpness(pil_img).enhance(1.15)

        else:
            pil_img = ImageEnhance.Contrast(pil_img).enhance(contrast_boost)
            pil_img = ImageEnhance.Sharpness(pil_img).enhance(sharpness_boost)
            pil_img = ImageEnhance.Color(pil_img).enhance(color_boost)

        output_path = output_dir / f"{uuid4().hex}_{mode}_{model_type}_restored.png"

        pil_img.save(output_path)

        return output_path



supir_service = SUPIRService()