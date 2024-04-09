import os
import re
from aiofile import async_open

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

async def stream_read_file(path: str, start, length):
    async with async_open(path,mode="rb") as file:
        file.seek(start)
        yield await file.read(length)

def compute_end_start_content_length(range_header: str, video_size: int):
    chunk_size: int = 10 ** 6 #1MB
    range_start: int = int(re.findall(r'\b\d+\b',range_header)[0])
    range_end: int = min(range_start + chunk_size, video_size - 1)
    return range_start, range_end, range_end - range_start + 1

@app.get("/")
async def root(request: Request):
    return {}

@app.get("/videos/{name}")
async def video(name: str, request: Request):
    return templates.TemplateResponse(request=request, name='index.html', context={"name": name})


@app.get("/stream/{name}")
async def stream(name: str,request: Request):
    #Check for range header
    if not request.headers['range']:
        return {}

    # get video name or id from endpoint path
    video_id = f'./{name}.mp4'
    video_size: int = os.stat(video_id).st_size
    print(video_size)
    start,end, length = compute_end_start_content_length(request.headers['range'], video_size)

    print(start,end, length)

    header_dict = {
        'Content-Range': f'bytes ${start}-${end}/${video_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(length),
        'Content-Type': 'video/mp4',
    }
    return StreamingResponse(stream_read_file(video_id, start, length),status_code=206,headers=header_dict ,media_type="application/octet-stream")
