import os
from functools import lru_cache
from dataclasses import dataclass
from fastapi.templating import Jinja2Templates

@dataclass
class Config:
    TEMPLATE_DIRECTORY: str = "templates"
    templates = Jinja2Templates(directory=TEMPLATE_DIRECTORY)
    local_video_dir = "."

@dataclass
class ProductionConfig(Config):
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://0.0.0.0:6379")
    POSTGRES_URL: str = ""
    local_video_dir = "/videos"

@dataclass
class TestingConfig(Config):
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://192.168.1.32:6379")
    POSTGRES_URL: str = ""

@lru_cache()
def get_settings():
    config_cls_dict = {
        "prd": ProductionConfig,
        "dev": TestingConfig
    }

    print(os.environ.get("FASTAPI_CONFIG", "dev"))
    config_name = os.environ.get("FASTAPI_CONFIG", "dev")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
