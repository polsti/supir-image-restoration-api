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
        try:
            upscale = int(upscale)
        except ValueError:
            upscale = 2

        if upscale not in [1, 2, 4]:
            upscale = 2

        if model_type == "Q":
            contrast_boost = 1.12
            sharpness_boost = 1.25
            color_boost = 1.06
            sharpen_strength = 0.65
        else:
            contrast_boost = 1.05
            sharpness_boost = 1.08
            color_boost = 1.02
            sharpen_strength = 0.35
            
        # 3 restoration model 
        # balanced - default, good for most images
        # strong - strong denoise, bigger contrast, sharpening
        # old photo - gray scale ? contrast boost 
        if mode == "strong":
            denoise_h = 5
            clahe_clip = 1.8
            sharpen_strength += 0.25
            contrast_boost += 0.08


        elif mode == "old_photo":
            denoise_h = 4
            clahe_clip = 1.5
            contrast_boost = 1.10
            sharpness_boost = 1.12
            color_boost = 1.0
            sharpen_strength = 0.25

        else:
            denoise_h = 3
            clahe_clip = 1.4
        # 1 mild denoise
        denoised = cv2.fastNlMeansDenoisingColored(
            image,
            None,
            h=denoise_h,
            hColor=denoise_h,
            templateWindowSize=7,
            searchWindowSize=21,
        )
        # 2 upscale
        height, width = denoised.shape[:2]
        upscaled = cv2.resize(
            denoised,
            (width * upscale, height * upscale),
            interpolation=cv2.INTER_LANCZOS4,
        )

        # 3 light contrast
        lab = cv2.cvtColor(upscaled, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=clahe_clip,
            tileGridSize=(8, 8),
        )

        l = clahe.apply(l)
        merged = cv2.merge((l, a, b))
        contrast = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

       
        # 4 stop crazy sharpening
        blur = cv2.GaussianBlur(
            #smooth,
            contrast, 
            (0, 0),
            sigmaX=1.0,
        )

        sharpened = cv2.addWeighted(
            contrast,
            1.0+ sharpen_strength,
            blur,
            - sharpen_strength,
            0,
        )

        #rgb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
        #pil_img = Image.fromarray(rgb)
        # optional old photo mode
        rgb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

        if mode == "old_photo":
            pil_img = ImageEnhance.Contrast(pil_img).enhance(1.10)
            pil_img = ImageEnhance.Sharpness(pil_img).enhance(1.12)
            pil_img = ImageEnhance.Color(pil_img).enhance(0.92)

        else:
            pil_img = ImageEnhance.Contrast(pil_img).enhance(contrast_boost)
            pil_img = ImageEnhance.Sharpness(pil_img).enhance(sharpness_boost)
            pil_img = ImageEnhance.Color(pil_img).enhance(color_boost)

        output_path = output_dir / f"{uuid4().hex}_{mode}_{model_type}_restored.png"
        pil_img.save(output_path)

        return output_path

supir_service = SUPIRService()