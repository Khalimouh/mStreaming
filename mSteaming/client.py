import time

import httpx

url = "http://127.0.0.1:8000/upload"
files = [("file", open("test.mp4", "rb"))]
data = {"name": "test.mp4", "format": "mp4", "quality": "1920x1080"}

with httpx.Client() as client:
    start = time.time()
    r = client.post(url, data=data, files=files)
    end = time.time()
    print(f"Time elapsed: {end - start}s")
    print(r.status_code, r.json(), sep=" ")
