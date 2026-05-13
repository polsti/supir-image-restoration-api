from pathlib import Path
from uuid import uuid4

import cv2
from PIL import Image, ImageEnhance


class SUPIRService:
    def __init__(self):
        self.model_loaded = False
        self.sr_model = None

    def load_model(self):
        model_path = Path("models/FSRCNN_x2.pb")

        if not model_path.exists():
            raise FileNotFoundError(
                "FSRCNN_x2.pb model was not found in models/ folder."
            )

        self.sr_model = cv2.dnn_superres.DnnSuperResImpl_create()
        self.sr_model.readModel(str(model_path))
        self.sr_model.setModel("fsrcnn", 2)

        print("FSRCNN x2 super-resolution model loaded.")
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

        # Model-based super-resolution
        if upscale == 1:
            restored = image.copy()

        elif upscale == 2:
            restored = self.sr_model.upsample(image)

        else:
            first_pass = self.sr_model.upsample(image)
            restored = self.sr_model.upsample(first_pass)

        # Q = quality-oriented, stronger visible enhancement
        # F = fidelity-oriented, softer and closer to original
        if model_type == "Q":
            contrast_boost = 1.12
            sharpness_boost = 1.20
            color_boost = 1.06
            sharpen_strength = 0.45
        else:
            contrast_boost = 1.04
            sharpness_boost = 1.05
            color_boost = 1.02
            sharpen_strength = 0.20

        if mode == "strong":
            denoise_h = 3
            clahe_clip = 1.6
            sharpen_strength += 0.20
            contrast_boost += 0.06

        elif mode == "old_photo":
            denoise_h = 2
            clahe_clip = 1.4
            contrast_boost = 1.08
            sharpness_boost = 1.08
            color_boost = 1.0
            sharpen_strength = 0.20

        else:
            denoise_h = 2
            clahe_clip = 1.3

        denoised = cv2.fastNlMeansDenoisingColored(
            restored,
            None,
            h=denoise_h,
            hColor=denoise_h,
            templateWindowSize=7,
            searchWindowSize=21,
        )

        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=clahe_clip,
            tileGridSize=(8, 8),
        )

        l = clahe.apply(l)
        merged = cv2.merge((l, a, b))
        contrast = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

        blur = cv2.GaussianBlur(
            contrast,
            (0, 0),
            sigmaX=1.0,
        )

        sharpened = cv2.addWeighted(
            contrast,
            1.0 + sharpen_strength,
            blur,
            -sharpen_strength,
            0,
        )

        rgb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

        pil_img = ImageEnhance.Contrast(pil_img).enhance(contrast_boost)
        pil_img = ImageEnhance.Sharpness(pil_img).enhance(sharpness_boost)

        if mode != "old_photo":
            pil_img = ImageEnhance.Color(pil_img).enhance(color_boost)

        output_path = output_dir / f"{uuid4().hex}_{mode}_{model_type}_restored.png"
        pil_img.save(output_path)

        return output_path


supir_service = SUPIRService()