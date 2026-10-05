from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from infra.api.routers import journey_routers
from infra.api.routers import index_routers

WEB_DIR = Path(__file__).parent / "web"

app = FastAPI()

app.include_router(journey_routers.router)
app.include_router(index_routers.router)
app.mount("/web", StaticFiles(directory=WEB_DIR), name="web")
