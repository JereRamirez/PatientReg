import os
from fastapi import UploadFile, HTTPException
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

UPLOAD_DIR = "../../uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

class InvalidFileExtensionException(Exception):
    pass

def save_file(file: UploadFile) -> str:
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_extension = file.filename.split(".")[-1]
        if file_extension not in ALLOWED_EXTENSIONS:
            raise InvalidFileExtensionException(f"Invalid file type {file_extension} for file {file.filename}")

        file_name = f"{uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        return f"/files/{file_name}"
    except InvalidFileExtensionException as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error saving file {file.filename}: {e}")
        return ""