import os
import sys

from fastapi import APIRouter
from fastapi import File,Form, Request, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from typing import Annotated, Dict, List
from config import settings
from service import videoService
from models import videoMetadata

videoRouter =  APIRouter()
videoService = videoService()

@videoRouter.get("/")
async def root(request: Request):
    return {}


@videoRouter.get("/videos/{name}")
async def video(name: str, request: Request):
    return settings.templates.TemplateResponse(
        request=request, name="index.html", context={"name": name}
    )


@videoRouter.get("/stream/{name}")
async def stream(name: str, request: Request):
    # Check for range header
    if not request.headers["range"]:
        return {}

    # get video name or id from endpoint path
    video_id = f"./{name}.mp4"
    video_size: int = os.stat(video_id).st_size
    start, end, length = videoService.compute_end_start_content_length(
        request.headers["range"], video_size
    )
    header_dict = {
        "Content-Range": f"bytes ${start}-${end}/${video_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(length),
        "Content-Type": "video/mp4",
    }
    return StreamingResponse(
        videoService.stream_read_file(video_id, start, length),
        status_code=206,
        headers=header_dict,
        media_type="videoRouterlication/octet-stream",
    )

@videoRouter.post("/upload")
async def upload_file(
    request: Request,
    name: Annotated[str, Form()],
    format: Annotated[str, Form()],
    quality: Annotated[str, Form()],
    file: UploadFile,
):
    if file.size >= 10000000000:
        raise HTTPException(status_code=500, detail="File too big to be processed")

    current_video_metadata = videoMetadata(name,format,quality)

    print(videoService.generate_video_formats_qualities(current_video_metadata))

    # write metadata to DB

    # Read file

    # run coversion tasks
    # write results to file storage




    await file.close()
    return {}
