from fastapi import APIRouter
from .service import calibrate
from .schema import CalibrateRequest, CalibrateResponse

router = APIRouter()


@router.post(
    "/calibrate",
    tags=["calibrate"],
    name="Perform Camera Calibration",
    responses={404: {"description": "Not found"}},
)
async def perform_calibration(calibrateRequest: CalibrateRequest) -> CalibrateResponse:
    """
    Perform camera calibration using the provided image and chessboard specifications.  
    Relies on [OpenCV's camera calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) functionality.  
    Input is a base64 encoded image of a chessboard pattern taken from the camera to be calibrated, along with the chessboard specifications and world points.  
    Returns the camera matrix, distortion coefficients, and inverted homography matrix which can be used for coordinate transformations.
    """
    calibrateResponse = calibrate(calibrateRequest)
    return calibrateResponse
