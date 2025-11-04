from fastapi import FastAPI
from .calibrate import router as calibrate
from .opencv import router as opencv
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI(
    title="Camera Calibration API",
    description="OpenCV Camera Calibration Functionality as REST API.",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)
app.include_router(calibrate.router)
app.include_router(opencv.router)


class HealthResponse(BaseModel):
    status: Annotated[
        str,
        Field(
            description="Health status of the server.",
            examples=["healthy"],
        ),
    ]


@app.get(
    "/health",
    tags=["health"],
    name="Health Check",
    description="Check server health status.",
)
async def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")
