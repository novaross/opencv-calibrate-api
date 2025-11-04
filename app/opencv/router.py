from fastapi import APIRouter
import cv2 as cv
from pydantic import BaseModel, Field
from typing import Annotated

router = APIRouter()


class CvVersion(BaseModel):
    openCvVersion: Annotated[
        str,
        Field(
            description="OpenCV version used in the application.",
            examples=["5.0.0alpha"],
        ),
    ]


@router.get(
    "/opencv/version",
    tags=["opencv"],
    name="Get OpenCV Version",
    description="Get OpenCV version used in the application.",
    responses={404: {"description": "Not found"}},
)
async def cv_version() -> CvVersion:
    cvVersion = CvVersion(openCvVersion=cv.__version__)
    return cvVersion
