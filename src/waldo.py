__author__ = 'ritchie'
import numpy as np
from pyimage import imutils
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-p","--puzzle", required = True,
                help = " Path to the puzzle image")
ap.add_argument("-w","--waldo", required = True,
                help = "Path to the waldo image")
args = vars(ap.parse_args())

puzzle = cv2.imread(args["puzzle"])
waldo = cv2.imread(args["waldo"])
waldo = imutils.resize(waldo,width=15)
(waldoHeight, waldoWidth) = waldo.shape[:2]

result = cv2.matchTemplate(puzzle,waldo,cv2.TM_CCOEFF)
(_,_,minLoc, maxLoc) = cv2.minMaxLoc(result)

# The puzzle image
topLeft = maxLoc
botRight = (topLeft[0]+waldoWidth,topLeft[1]+waldoHeight)
roi = puzzle[topLeft[1]:botRight[1], topLeft[0]:botRight[0]]

# Construct a darkened transparent 'layer' to darken everything
# in the puzzle except for waldo
mask = np.zeros(puzzle.shape,dtype="uint8")
puzzle = cv2.addWeighted(puzzle,0.25,mask,0.75,0)

# Put the original waldo back in the image so that he is
# 'brighter' than the rest of the image
puzzle[topLeft[1]:botRight[1],topLeft[0]:botRight[0]] = roi

#Display the images
cv2.imshow("Puzzle", imutils.resize(puzzle,height=650))
cv2.imshow("Waldo", waldo)
cv2.waitKey(0)