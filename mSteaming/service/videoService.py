import re

from aiofile import async_open
from itertools import product
from typing import List
from models import videoMetadata

class videoService():
    def __init__(self) -> None:
        self.quality = ["1920x1080", "1280x720"]
        self.formats = ["flv", "mp4"]

    def generate_video_formats_qualities(self,initialMetadata: videoMetadata) -> List[videoMetadata]:
        all_formats = []
        combined_format_qualities = product(self.quality, self.formats)
        for data in combined_format_qualities:
            if (data[0] != initialMetadata.quality and data[1] != initialMetadata.format) or data[0] != initialMetadata.quality or data[1] != initialMetadata.format:
                all_formats.append(videoMetadata(initialMetadata.name,data[1], data[0]))
        return all_formats


    def create_video_names(self, input :List[videoMetadata]) -> List[videoMetadata]:
        return [videoMetadata(x.name, x.format, x.quality, x.videoid, f"${x.name}_${x.quality}.${x.format}") for x in input]


    def compute_end_start_content_length(self,range_header: str, video_size: int):
        chunk_size: int = 10**6  # 1MB
        range_start: int = int(re.findall(r"\b\d+\b", range_header)[0])
        range_end: int = min(range_start + chunk_size, video_size - 1)
        return range_start, range_end, range_end - range_start + 1

    async def stream_read_file(self,path: str, start, length):
        async with async_open(path, mode="rb") as file:
            file.seek(start)
            yield await file.read(length)
