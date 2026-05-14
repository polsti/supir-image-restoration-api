from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from PIL import Image


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MIN_DIMENSION = 500


def validate_image_file(file: UploadFile) -> str:
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG images are supported."
        )

    return extension

def validate_image_size(file_path: Path) -> None:
    image = Image.open(file_path)
    width, height = image.size

    if width < MIN_DIMENSION or height < MIN_DIMENSION:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Image is too small ({width}x{height}). "
                f"Both width and height must be at least {MIN_DIMENSION} pixels."
            )
        )


async def save_uploaded_image(file: UploadFile, input_dir: Path) -> Path:
    extension = validate_image_file(file)

    input_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid4().hex}{extension}"
    file_path = input_dir / file_name

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path