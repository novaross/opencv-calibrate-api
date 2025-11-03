from pydantic import BaseModel
from typing import List


class ChessboardSpec(BaseModel):
    rows: int
    columns: int
    squareSizeMm: int


class Point(BaseModel):
    x: int
    y: int


class CalibrateRequest(BaseModel):
    imageBase64: str
    chessboardSpec: ChessboardSpec
    worldPoints: List[Point]


class CalibrateResponse(BaseModel):
    message: str
    cameraMatrix: List[List[float]]
    dist: List[float]
    hmi: List[float]
