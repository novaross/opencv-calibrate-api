import numpy as np
import cv2 as cv
import base64
from app.logger import app_logger as log


def calibrate_camera(img, chessboard_spec):
    # parameters based on real chessboard dimensions
    board_grid_x = chessboard_spec.columns
    board_grid_y = chessboard_spec.rows
    square_size_mm = chessboard_spec.squareSizeMm

    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((board_grid_x * board_grid_y, 3), np.float32)
    objp[:, :2] = (
        np.mgrid[0:board_grid_x, 0:board_grid_y].T.reshape(-1, 2) * square_size_mm
    )

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    log.debug("Looking for chessboard corners...")
    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, (board_grid_x, board_grid_y), None)
    if ret == True:
        log.debug("Found corners")
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None
        )
        return mtx, dist, objpoints, imgpoints
    else:
        log.warning("Could not find corners in image")
        # todo: raise exception
        return None


def create_image_with_detected_corners(image, corners, chessboard_spec):
    board_grid_x = chessboard_spec.columns
    board_grid_y = chessboard_spec.rows
    cv.drawChessboardCorners(image, (board_grid_x, board_grid_y), corners, True)
    return image


def find_chessboard_corners(image, chessboard_spec):
    board_grid_x = chessboard_spec.columns
    board_grid_y = chessboard_spec.rows
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, (board_grid_x, board_grid_y), None)
    if ret:
        corners = cv.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001),
        )
        return corners
    else:
        log.debug("Chessboard not detected in the image.")
        return None


def undistort_image(image, mtx, dist):
    h, w = image.shape[:2]
    new_mtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    undistorted = cv.undistort(image, mtx, dist, None, new_mtx)
    return undistorted, new_mtx


def find_homography(world_points_mm, imgpoints):
    # convert world_points_mm to objpoints
    # array of objects to np.array
    point_tuples = [[point.x, point.y] for point in world_points_mm]
    objpoints = np.array(point_tuples, dtype=np.float32)

    """
    Compute homography from real-world 3D points (in mm) to 2D image points.
    Note: Since chessboard is flat, we use z=0 for all points.
    """
    # Use only the x, y coordinates (z=0)
    objpoints_2d = objpoints[:, :2]  # (N, 2) in mm
    imgpoints_2d = imgpoints[:, :2]  # (N, 2) in pixels

    # Compute homography matrix H: pixel = H * world
    homography_matrix, _ = cv.findHomography(objpoints_2d, imgpoints_2d, cv.RANSAC, 5.0)
    return homography_matrix


def invert_homography(homography_matrix):
    homography_matrix_inverted = np.linalg.inv(homography_matrix)
    return homography_matrix_inverted


def draw_points_on_image(image, points, radius=3, color=(0, 0, 255), thickness=-1):
    # Create a copy of the image to avoid modifying the original
    image_with_points = image.copy()

    # Convert points to list if it's a numpy array
    if isinstance(points, np.ndarray):
        points = points.reshape(-1, 2)

    # Draw each point
    for point in points:
        x, y = int(point[0]), int(point[1])
        cv.circle(image_with_points, (x, y), radius, color, thickness)

    return image_with_points


def convertBase64ToImage(imageBase64: str):
    image_data = base64.b64decode(imageBase64)
    np_arr = np.frombuffer(image_data, np.uint8)
    image = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    return image
