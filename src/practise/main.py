__author__ = 'ritchie'
import argparse

import numpy as np
import cv2

from src.pyimage import transform

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",help = "path to the images file")
ap.add_argument("-c","--coords", help = "comma separated list of source points")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]),dtype="float32")

warped = transform.four_point_transform(image, pts)

cv2.imshow("Original",image)
cv2.imshow("Warped",warped)
cv2.waitKey(0)
