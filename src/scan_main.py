__author__ = 'ritchie'

# Import the necessary packages
import argparse
from skimage.filter import threshold_adaptive
from pyimage.transform import four_point_transform
from pyimage import imutils
import cv2


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required = True,
                help = "Path to the image to be scanned")
ap.add_argument("-o","--out",required=True,
                help = " Path to the image to be saved")
ap.add_argument("-s","--size",required=True,
                help = "Size of the image to be saved")
args = vars(ap.parse_args())

size = int(args["size"])
out = args["out"]

# edge detection
image = cv2.imread(args["image"])
ratio = image.shape[0]/500.0
orig = image.copy()
image = imutils.resize(image,height=500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5),0)
edged = cv2.Canny(gray,75,200)

print "STEP 1: Edge Detection:"
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Finding Countours
(cnts,_)=cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:5]

for c in cnts:
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.02*peri,True)

    if len(approx) == 4:
        screenCnt = approx
        break

print "STEP 2: Find contours of paper:"
cv2.drawContours(image,[screenCnt],-1,(0,255,0),2)
cv2.imshow("Outline",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply a Perspective Tranform & Threshold
warped = four_point_transform(orig,screenCnt.reshape(4,2)*ratio)

warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped,250,offset=10)
warped = warped.astype("uint8")*255

print "STEP 3: Apply perspective transform"
cv2.imshow("Original",imutils.resize(orig,height = size))
cv2.imshow("Scanned",imutils.resize(warped,height = size))

cv2.imwrite(out, warped)
cv2.waitKey(0)