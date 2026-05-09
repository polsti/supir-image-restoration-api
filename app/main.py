from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form

from app.utils import save_uploaded_image


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "inputs"


app = FastAPI(
    title="SUPIR Image Restoration API",
    description="REST API for image restoration and super-resolution using SUPIR.",
    version="0.2.0",
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
):
    saved_path = await save_uploaded_image(image, INPUT_DIR)

    return {
        "message": "Image uploaded successfully",
        "original_filename": image.filename,
        "saved_filename": saved_path.name,
        "saved_path": str(saved_path),
        "upscale": upscale,
    }