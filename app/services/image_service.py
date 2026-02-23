import os
import uuid
import io
import time
from datetime import datetime
from PIL import Image
from fastapi import UploadFile, HTTPException
from app.utils.logger import logger
from app.services.caption_service import generate_caption

# ===== In-Memory Storage =====
images_db = {}
processing_times = []

# ===== Directory Setup =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
THUMBNAIL_DIR = os.path.join(BASE_DIR, "thumbnails")
os.makedirs(THUMBNAIL_DIR, exist_ok=True)


# ===============================
# Upload + Processing Logic
# ===============================
async def process_upload(file: UploadFile):

    start_time = time.time()
    image_id = str(uuid.uuid4())
    processed_time = datetime.utcnow().isoformat() + "Z"

    logger.info(f"Upload started: {file.filename}")

    contents = await file.read()

    # Validate actual image (magic bytes check)
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
        img = Image.open(io.BytesIO(contents))
    except Exception:
        logger.error("Invalid or corrupted image file")

        failed_response = {
            "status": "failed",
            "data": {
                "image_id": image_id,
                "original_name": file.filename,
                "processed_at": processed_time,
                "metadata": {},
                "thumbnails": {}
            },
            "error": "invalid image file"
        }

        images_db[image_id] = failed_response
        return failed_response

    # Only allow JPEG and PNG
    if img.format not in ["JPEG", "PNG"]:
        logger.warning("Unsupported file format")

        failed_response = {
            "status": "failed",
            "data": {
                "image_id": image_id,
                "original_name": file.filename,
                "processed_at": processed_time,
                "metadata": {},
                "thumbnails": {}
            },
            "error": "invalid file format"
        }

        images_db[image_id] = failed_response
        return failed_response

    width, height = img.size
    # Calculate proportional sizes
    medium_size = (int(width * 0.5), int(height * 0.5))
    small_size = (int(width * 0.25), int(height * 0.25))
    extension = img.format.lower()
    format_map = {
        "jpeg": "jpg",
        "png": "png"
    }

    display_format = format_map.get(extension, extension)

    # ---- MEDIUM (50%) ----
    medium_img = img.copy()
    medium_img = medium_img.resize(medium_size)

    medium_path = os.path.join(
        THUMBNAIL_DIR, f"{image_id}_medium.{extension}"
    )
    medium_img.save(medium_path, format=img.format)
    caption = generate_caption(medium_path)

    # ---- SMALL (25%) ----
    small_img = img.copy()
    small_img = small_img.resize(small_size)

    small_path = os.path.join(
        THUMBNAIL_DIR, f"{image_id}_small.{extension}"
    )
    small_img.save(small_path, format=img.format)

    end_time = time.time()
    processing_time = end_time - start_time
    processing_times.append(processing_time)

    logger.info(f"Image processed successfully: {image_id}")

    response = {
        "status": "success",
        "data": {
            "image_id": image_id,
            "original_name": file.filename,
            "processed_at": processed_time,
            "metadata": {
                "width": width,
                "height": height,
                "format": display_format,
                "size_bytes": len(contents),
                "caption": caption
            },
            "thumbnails": {
                "small": f"/api/images/{image_id}/thumbnails/small",
                "medium": f"/api/images/{image_id}/thumbnails/medium"
            }
        },
        "error": None
    }

    images_db[image_id] = response
    return response


# ===============================
# Read Operations
# ===============================
def get_all_images():
    return list(images_db.values())


def get_image_by_id(image_id: str):
    if image_id not in images_db:
        raise HTTPException(status_code=404, detail="Image not found")
    return images_db[image_id]


def get_thumbnail_path(image_id: str, size: str):
    if size not in ["small", "medium"]:
        raise HTTPException(status_code=400, detail="Invalid size")

    if image_id not in images_db:
        raise HTTPException(status_code=404, detail="Image not found")

    extension = images_db[image_id]["data"]["metadata"]["format"].lower()

    path = os.path.join(
        THUMBNAIL_DIR, f"{image_id}_{size}.{extension}"
    )

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Thumbnail not found")

    return path


def get_stats():
    total = len(images_db)
    failed = len([img for img in images_db.values() if img["status"] == "failed"])
    success = total - failed

    success_rate = f"{(success / total) * 100:.2f}%" if total > 0 else "0%"

    avg_time = (
        sum(processing_times) / len(processing_times)
        if processing_times else 0
    )

    return {
        "total": total,
        "failed": failed,
        "success_rate": success_rate,
        "average_processing_time_seconds": round(avg_time, 2)
    }
