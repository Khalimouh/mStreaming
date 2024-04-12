import os
import re
import time
from typing import Annotated

from aiofile import async_open
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from celery.app import Celery

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
redis_url = os.getenv("REDIS_URL", "redis://192.168.1.32:6379")
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)
templates = Jinja2Templates(directory="templates")

@celery_app.task()
def write_task():
    time.sleep(1000)
    return "Hello"

async def stream_read_file(path: str, start, length):
    async with async_open(path, mode="rb") as file:
        file.seek(start)
        yield await file.read(length)


def compute_end_start_content_length(range_header: str, video_size: int):
    chunk_size: int = 10**6  # 1MB
    range_start: int = int(re.findall(r"\b\d+\b", range_header)[0])
    range_end: int = min(range_start + chunk_size, video_size - 1)
    return range_start, range_end, range_end - range_start + 1


@app.get("/")
async def root(request: Request):
    return {}


@app.get("/videos/{name}")
async def video(name: str, request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"name": name}
    )


@app.get("/stream/{name}")
async def stream(name: str, request: Request):
    # Check for range header
    if not request.headers["range"]:
        return {}

    # get video name or id from endpoint path
    video_id = f"./{name}.mp4"
    video_size: int = os.stat(video_id).st_size
    print(video_size)
    start, end, length = compute_end_start_content_length(
        request.headers["range"], video_size
    )

    print(start, end, length)

    header_dict = {
        "Content-Range": f"bytes ${start}-${end}/${video_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(length),
        "Content-Type": "video/mp4",
    }
    return StreamingResponse(
        stream_read_file(video_id, start, length),
        status_code=206,
        headers=header_dict,
        media_type="application/octet-stream",
    )

@app.post("/upload")
async def upload_file(
    request: Request,
    name: Annotated[str, Form()],
    format: Annotated[str, Form()],
    quality: Annotated[str, Form()],
    file: UploadFile = File(),
):
    print(file)
    # Generate metadata

    # write metadata to import debugpy, platform
    # Read file

    # run coversion tasks
    t = write_task.delay()
    print(t.status)
    # write results to file storage
    return {}
