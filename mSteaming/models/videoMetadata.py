from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class videoMetadata:
    name: str
    format: str
    quality: str
    videoid: UUID = uuid4()
    videoFilePath: str = ""
