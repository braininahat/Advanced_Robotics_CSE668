from __future__ import print_function
import numpy as np
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# images = glob.glob('*.jpg')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

count = 0

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture,
                                       format="bgr",
                                       use_video_port=True):
    # and occupied/unoccupied text
    img = frame.array

    img = cv2.pyrDown(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('img', gray)
    cv2.waitKey(1)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        count += 1

        corners2 = cv2.cornerSubPix(gray,
                                    corners,
                                    (11, 11),
                                    (-1, -1),
                                    criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(gray, (7, 6), corners2, ret)
        cv2.imshow('img', gray)
        cv2.waitKey(1)

    rawCapture.truncate(0)

    print(count)

    if count == 30:
        break

rms, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints,
                                                                    imgpoints,
                                                                    gray.shape[::-1],
                                                                    None,
                                                                    None)

print("\nrms\n", rms)
print("\ncamera_matrix\n", camera_matrix)
print("\ndist_coeffs\n", dist_coeffs)
print("\nrvecs\n", rvecs)
print("\ntvecs\n", tvecs)

# dist_coeffs gives k1 k2 p1 p2
# camera matrix 00 is fx 11 is fy 20 p1 21 p2 (maybe)

cv2.destroyAllWindows()
