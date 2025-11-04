from pydantic import BaseModel, Field
from typing import List
from typing import Annotated


class ChessboardSpec(BaseModel):
    """
    Parameters for chessboard which is used for calibration.
    """

    rows: Annotated[
        int,
        Field(description="Number of inner corners per chessboard row.", examples=[3]),
    ]
    columns: Annotated[
        int,
        Field(
            description="Number of inner corners per chessboard column.", examples=[4]
        ),
    ]
    squareSizeMm: Annotated[
        int, Field(description="Size of a chessboard square in mm.", examples=[82])
    ]


class Point(BaseModel):
    x: int
    y: int


class CalibrateRequest(BaseModel):
    imageBase64: Annotated[
        str,
        Field(
            description="Base64 encoded image obtained from the camera intended for calibration.",
            examples=["iVBORw0KGgoAAAANSUhEUgAA..."],
        ),
    ]
    chessboardSpec: ChessboardSpec
    worldPoints: Annotated[
        List[Point],
        Field(
            description="World points representing physical coordinates of chessboard corners, measured in millimeters.\n\n"
            + "The amounts of points should match the number of inner corners defined by the chessboardSpec.\n\n",
            examples=[
                [Point(x=600, y=274), Point(x=681, y=274), Point(x=673, y=274)],
                [Point(x=845, y=274), Point(x=600, y=356), Point(x=673, y=356)],
            ],
        ),
    ]


class CalibrateResponse(BaseModel):
    message: str
    mtx: Annotated[
        List[List[float]],
        Field(
            description="Camera Matrix from the calibration process",
            examples=[
                [[1351.8, 0.0, 673.0], [0.0, 1191.3, 239.0], [0.0, 0.0, 1.0]],
            ],
        ),
    ]
    dist: Annotated[
        List[float],
        Field(
            description="Distortion coefficients from the calibration process",
            examples=[
                [-0.491, 25.912, 0.009, 0.024, -327.35],
            ],
        ),
    ]
    hm: Annotated[
        List[float],
        Field(
            description="Homography Matrix from the calibration process",
            examples=[
                [0.54, -0.10, -39.11, 0.01, 0.46, 72.00, 4.55, -0.01, 1.00],
            ],
        ),
    ]
    hmi: Annotated[
        List[float],
        Field(
            description="Homography Matrix Inverted from the calibration process",
            examples=[
                [1.80, 0.45, 38.15, -0.04, 2.05, -149.71, -9.45, 0.01, 0.95],
            ],
        ),
    ]
