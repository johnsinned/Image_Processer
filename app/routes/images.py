from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.image_service import (
    process_upload,
    get_all_images,
    get_image_by_id,
    get_thumbnail_path,
    get_stats
)

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    return await process_upload(file)

@router.get("/api/images")
def list_images():
    return get_all_images()

@router.get("/api/images/{image_id}")
def get_image(image_id: str):
    return get_image_by_id(image_id)

@router.get("/api/images/{image_id}/thumbnails/{size}")
def get_thumbnail(image_id: str, size: str):
    path = get_thumbnail_path(image_id, size)
    return FileResponse(path)

@router.get("/api/stats")
def stats():
    return get_stats()
