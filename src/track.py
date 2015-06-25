__author__ = 'ritchie'

import numpy as np
import argparse
import cv2

# Initialize the current frame of the video, along with the list
# of ROI points along with whether or not this is input mode
frame = None        # Current frame of the video being processed
roiPts = []         # List of points corresponding to the Region of Interest in video
inputMode = False   # Indicate whether or not we're selecting the object we want to track

def selectROI(event, x, y, flags, param):
    # Get the reference to the current frame, list of ROI
    # points and whether or not it's ROI selection mode
    global frame, roiPts, inputMode

    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts)<4:
        roiPts.append((x,y))
        cv2.circle(frame, (x,y), 4,(0,255,0),2)
        cv2.imshow("frame",frame)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v","--video",
                    help = "path to the (optional) video file")
    args = vars(ap.parse_args())

    global frame, roiPts, inputMode

    if not args.get("video", False):
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(args["video"])

    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)

    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1)
    roiBox = None

    while True:
        (grabbed, frame) = camera.read()

        if not grabbed:
            break

        if roiBox is not None:
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            backProj = cv2.calcBackProject([hsv], [0], roiHist, [0,180], 1)

            (r,roiBox)=cv2.CamShift(backProj,roiBox,termination)
            pts = np.intii0(cv2.cv.BoxPoints(r))
            cv2.polylines(frame,[pts],True,(0,255,0),2)

        cv2.imshow("frame",frame)
        key = cv2.waitKey(1) & 0XFF

        if key == ord("i") and len(roiPts) <4 :
            inputMode = True
            orig = frame.copy()

            while len(roiPts) <4 :
                cv2.imshow("frame",frame)
                cv2.waitKey(0)

            roiPts = np.array(roiPts)
            s = roiPts.sum(axis=1)
            tl = roiPts[np.argmin(s)]
            br = roiPts[np.argmax(s)]

            roi = orig[tl[1]:br[1],tl[0]:br[0]]
            roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

            roiHist = cv2.calcHist([roi],[0],None, [16],[0,180])
            roiHist = cv2.normalize(roiHist,roiHist, 0,255,cv2.NORM_MINMAX)
            roiBox = (tl[0],tl[1],br[0],br[1])
        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()