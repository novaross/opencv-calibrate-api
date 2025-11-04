from app.calibrate import utils
from .schema import CalibrateRequest, CalibrateResponse
from .utils import *
from app.logger import app_logger as log


def calibrate(calibrateRequest: CalibrateRequest):
    calibration_image_base64 = calibrateRequest.imageBase64
    log.debug("Calibrate request received")
    image = convertBase64ToImage(calibration_image_base64)
    chessboard_spec = calibrateRequest.chessboardSpec

    # get calibration parameters based on image
    mtx, dist, objpoints, imgpoints = utils.calibrate_camera(image, chessboard_spec)
    log.debug("mtx: {}".format(mtx))
    log.debug("dist: {}".format(dist))

    image_with_corners = utils.create_image_with_detected_corners(
        image, imgpoints[0], chessboard_spec
    )
    output_path = "output/image_detected_corners.jpg"
    log.debug("Writing image with detected corners to: {}".format(output_path))
    cv.imwrite(output_path, image_with_corners)

    # un distort and detect corners on the undistorted image
    undistorted_image, new_mtx = utils.undistort_image(image, mtx, dist)
    detected_corners = utils.find_chessboard_corners(undistorted_image, chessboard_spec)

    # calculate the homography matrix
    world_points_mm = calibrateRequest.worldPoints
    log.debug("Calculating homography matrix...")
    homography_matrix = utils.find_homography(world_points_mm, detected_corners)
    log.debug("Homography Matrix: {}".format(homography_matrix))

    hmi = utils.invert_homography(homography_matrix)
    log.debug("Homography Matrix Inverted: {}".format(hmi))

    # format output
    decimal_places = 10
    format_spec = f".{decimal_places}f"
    mtx_formatted = [[f"{v:{format_spec}}" for v in row] for row in mtx.tolist()]
    dist_formatted = [f"{v:{format_spec}}" for v in dist.flatten().tolist()]
    hm_formatted = [f"{v:{format_spec}}" for v in homography_matrix.flatten().tolist()]
    hmi_formatted = [f"{v:{format_spec}}" for v in hmi.flatten().tolist()]

    calibrateResponse = CalibrateResponse(
        message="Calibration performed successfully",
        mtx=mtx_formatted,
        dist=dist_formatted,
        hm=hm_formatted,
        hmi=hmi_formatted,
    )

    return calibrateResponse
