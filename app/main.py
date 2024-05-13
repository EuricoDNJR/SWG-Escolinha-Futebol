import os

import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.v1 import teams, users, responsibles, students

from .utils.helper import logging

dotenv.load_dotenv()


ENV = os.getenv("ENV")

api_version = "v0.1.0"
route_version = "v1"

api_metadata = {
    "title": "SWG - Escolhinha de Futebol FARP",
    "description": "API de gerenciamento da escolhinha de futebol FARP",
    "version": api_version,
}

if ENV == "dev":
    app = FastAPI(
        title=api_metadata["title"],
        description=api_metadata["description"],
        version=api_metadata["version"],
    )
else:
    app = FastAPI(
        title=api_metadata["title"],
        description=api_metadata["description"],
        version=api_metadata["version"],
        # docs_url=None,
        # redoc_url=None,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

response_404 = {404: {"description": "Not found"}}

app.include_router(
    users.router,
    prefix=f"/{route_version}",
    tags=["users"],
    responses=response_404,
)

app.include_router(
    responsibles.router,
    prefix=f"/{route_version}",
    tags=["responsibles"],
    responses=response_404,
)

app.include_router(
    teams.router,
    prefix=f"/{route_version}",
    tags=["teams"],
    responses=response_404,
)

app.include_router(
    students.router,
    prefix=f"/{route_version}",
    tags=["students"],
    responses=response_404,
)

@app.get(
    "/",
    responses={
        200: {
            "description": "Root",
            "content": {"application/json": {"example": {"api-version": api_version}}},
        }
    },
)
async def root():
    logging.info("Receiving request to root")
    return {"api-version": api_version}