from fastapi import FastAPI

from infra.api.routers import journey_routers

app = FastAPI()

app.include_router(journey_routers.router)
