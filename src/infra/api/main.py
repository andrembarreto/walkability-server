from fastapi import FastAPI

from infra.api.routers import journey_routers
from infra.api.routers import index_routers

app = FastAPI()

app.include_router(journey_routers.router)
app.include_router(index_routers.router)
