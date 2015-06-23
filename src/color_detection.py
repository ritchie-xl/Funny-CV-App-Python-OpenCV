__author__ = 'ritchie'
import numpy as np
import argparse
import cv2
from pyimage import imutils

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",
                help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
resized = imutils.resize(image, height=400)

boundaries = [
    ([17,15,100],[50,56,200]),  #red
    ([86,31,4],[220,88,50]),    #blue
    ([25,146,190],[62,174,250]),#yellow
    ([103,86,35],[145,133,128]) #gray
]

for(lower, upper) in boundaries:
    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')

    mask = cv2.inRange(resized, lower, upper)
    output = cv2.bitwise_and(resized, resized, mask=mask)

    cv2.imshow("Images",np.hstack([resized,output]))
    cv2.waitKey(0)