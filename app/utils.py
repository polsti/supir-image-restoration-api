from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, HTTPException


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def validate_image_file(file: UploadFile) -> str:
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG images are supported."
        )

    return extension


async def save_uploaded_image(file: UploadFile, input_dir: Path) -> Path:
    extension = validate_image_file(file)

    input_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid4().hex}{extension}"
    file_path = input_dir / file_name

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path