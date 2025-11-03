from fastapi import APIRouter
from .service import calibrate
from .schema import CalibrateRequest

router = APIRouter()


@router.post(
    "/calibrate",
    tags=["calibrate"],
    responses={404: {"description": "Not found"}},
)
async def perform_calibration(calibrateRequest: CalibrateRequest):
    calibrateResponse = calibrate(calibrateRequest)
    return calibrateResponse
