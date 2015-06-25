__author__ = 'ritchie'
import cv2
import numpy as np

def translate(image, x,y):
    M = np.float32([1,0,x],[0,1,y])
    shifted = cv2.warpPerspective(image, M, (image.shape[1], image.shap[0]))
    return shifted

def rotate(image,angle, center= None, scale = 1.0):
    (h,w) = image.shape[:2]

    if center is None:
        center = (w/2,h/2)

    M = cv2.getRotationMatrix2D(center, angle,scale)
    rotated = cv2.warpPerspective(image, M, (w,h))

    return rotated


def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height/float(h)
        dim = (int(w*r),height)
    else:
        r = width/(float(w))
        dim = (width,int(h*r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized

def centroid_histogram(clt):
    numLabels = np.arange(0,len(np.unique(clt.labels_))+1)
    (hist,_) = np.histogram(clt.labels_,bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors(hist, centroids):
    bar = np.zeros((50,300,3),dtype="uint8")
    startX=0

    for(percent,color) in zip(hist,centroids):
        endX = startX + (percent*300)
        cv2.rectangle(bar,(int(startX),0), (int(endX),50),
                      color.astype("uint8").tolist(),-1)
        startX = endX

    return bar