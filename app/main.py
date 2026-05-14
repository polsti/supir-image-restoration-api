from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse

from app.utils import save_uploaded_image, validate_image_size
from app.supir_service import supir_service


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "inputs"
OUTPUT_DIR = BASE_DIR / "outputs"


app = FastAPI(
    title="SUPIR Image Restoration API",
    description="REST API for image restoration and super-resolution using SUPIR.",
    version="0.4.0",
)


@app.get("/")
def root():
    return {
        "message": "SUPIR Image Restoration API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/restore")
async def restore_image(
    image: UploadFile = File(...),
    upscale: int = Form(2),
    mode: str = Form("mock"),
    model_type: str = Form("Q"),
):
    if upscale not in [1, 2, 4]:
        return {
            "error": "Upscale must be 1, 2, or 4"
        }

    saved_path = await save_uploaded_image(image, INPUT_DIR)
    validate_image_size(saved_path)

    output_path = supir_service.restore_image(
        input_path=saved_path,
        output_dir=OUTPUT_DIR,
        upscale=upscale,
        mode=mode,
        model_type=model_type,
    )

    return FileResponse(
        path=str(output_path),
        media_type="image/png",
        filename="restored_image.png",
    )