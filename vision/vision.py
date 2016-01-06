import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # define range of red color in HSV
    lower_red = np.array([17, 15, 100], dtype=np.uint8)
    upper_red = np.array([50, 56, 200], dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(frame, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()