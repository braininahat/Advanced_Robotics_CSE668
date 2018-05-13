import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# images = glob.glob('*.jpg')

cap = cv2.VideoCapture(0)
count = 0
while count <= 30:
    ret, img = cap.read()
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
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,
                                                           imgpoints,
                                                           gray.shape[::-1],
                                                           None,
                                                           None)
        print("\n", ret)
        print("\n", mtx)
        print("\n", dist)
        print("\n", rvecs)
        print("\n", tvecs)

cv2.destroyAllWindows()
