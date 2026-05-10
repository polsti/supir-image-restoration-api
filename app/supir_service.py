from pathlib import Path
from uuid import uuid4
import subprocess
import shutil

from PIL import Image, ImageEnhance


class SUPIRService:
    def __init__(self):
        self.model_loaded = False

        self.base_dir = Path(__file__).resolve().parents[1]
        self.external_supir_dir = self.base_dir / "external" / "SUPIR"

    def load_model(self):
        """
        Placeholder for real model loading.

        Current integration uses SUPIR through its official test.py script,
        so the actual model is loaded inside the subprocess.
        """
        print("SUPIR subprocess integration is ready.")
        self.model_loaded = True

    def mock_restore_image(
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
        new_size = (width * upscale, height * upscale)

        restored = image.resize(new_size, Image.Resampling.LANCZOS)

        sharpness = ImageEnhance.Sharpness(restored)
        restored = sharpness.enhance(1.5)

        contrast = ImageEnhance.Contrast(restored)
        restored = contrast.enhance(1.1)

        output_path = output_dir / f"{uuid4().hex}_mock_restored.png"
        restored.save(output_path)

        return output_path

    def restore_with_supir(
        self,
        input_path: Path,
        output_dir: Path,
        upscale: int = 2,
        model_type: str = "Q",
    ) -> Path:
        if not self.external_supir_dir.exists():
            raise FileNotFoundError(
                "SUPIR repository was not found. Expected path: "
                f"{self.external_supir_dir}"
            )

        job_id = uuid4().hex

        job_input_dir = self.base_dir / "inputs" / f"supir_job_{job_id}"
        job_output_dir = output_dir / f"supir_job_{job_id}"

        job_input_dir.mkdir(parents=True, exist_ok=True)
        job_output_dir.mkdir(parents=True, exist_ok=True)

        copied_input_path = job_input_dir / input_path.name
        shutil.copy(input_path, copied_input_path)

        command = [
            "python",
            "test.py",
            "--img_dir",
            str(job_input_dir),
            "--save_dir",
            str(job_output_dir),
            "--upscale",
            str(upscale),
            "--SUPIR_sign",
            model_type,
        ]

        result = subprocess.run(
            command,
            cwd=str(self.external_supir_dir),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "SUPIR inference failed.\n\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            )

        output_images = list(job_output_dir.glob("*.png")) + list(job_output_dir.glob("*.jpg"))

        if not output_images:
            raise RuntimeError("SUPIR finished, but no output image was generated.")

        return output_images[0]

    def restore_image(
        self,
        input_path: Path,
        output_dir: Path,
        upscale: int = 2,
        mode: str = "mock",
        model_type: str = "Q",
    ) -> Path:
        if mode == "supir":
            return self.restore_with_supir(
                input_path=input_path,
                output_dir=output_dir,
                upscale=upscale,
                model_type=model_type,
            )

        return self.mock_restore_image(
            input_path=input_path,
            output_dir=output_dir,
            upscale=upscale,
        )


supir_service = SUPIRService()