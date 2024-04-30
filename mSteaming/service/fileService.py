
from os import lseek
from pathlib import Path
from typing import List
from config import Config, settings


class fileService():
    def __init__(self, conf: Config) -> None:
        self.rootVideoStr = conf.local_video_dir
        self.rootVideoPath = Path(self.rootVideoStr)

    def listVideos(self) -> List[str]:
        return [x.name for x in self.rootVideoPath.iterdir()]

    def __repr__(self) -> str:
        return f"{self} : (path: {self.rootVideoStr})"






