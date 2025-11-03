from fastapi import APIRouter
import cv2 as cv

router = APIRouter()


@router.get(
    "/opencv/version",
    tags=["opencv_version"],
    responses={404: {"description": "Not found"}},
)
async def cv_version():
    return {"cv version": cv.__version__}
