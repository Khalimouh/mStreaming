import sys

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from routers.videoRouter import videoRouter


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("app init")
    yield
    print("app cleanup")

app = FastAPI(lifespan=app_lifespan)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(videoRouter)






