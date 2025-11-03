from app.calibrate import utils
from .schema import CalibrateRequest, CalibrateResponse
from .utils import *
from app.logger import app_logger as log


def calibrate(calibrateRequest: CalibrateRequest):
    calibration_image_base64 = calibrateRequest.imageBase64
    log.debug("Calibrate request received")
    image = convertBase64ToImage(calibration_image_base64)
    chessboard_spec = calibrateRequest.chessboardSpec
    world_points_mm = calibrateRequest.worldPoints

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
    log.debug("new_mtx: {}".format(new_mtx))
    detected_pixel_corners = utils.find_chessboard_corners(
        undistorted_image, chessboard_spec
    )

    # calculate the homography matrix
    log.debug("Calculating homography matrix...")
    homography_matrix = utils.compute_homography(
        world_points_mm, detected_pixel_corners
    )
    log.debug("Homography Matrix: {}".format(homography_matrix))

    homography_matrix_inverted = utils.invert_homography(homography_matrix)
    log.debug("Homography Matrix Inverted: {}".format(homography_matrix_inverted))

    calibrateResponse = CalibrateResponse(
        message="Calibration performed successfully",
        cameraMatrix=mtx.tolist(),
        dist=dist.flatten().tolist(),
        hmi=homography_matrix_inverted.flatten().tolist()
    )

    return calibrateResponse
