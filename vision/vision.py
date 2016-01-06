import cv2
import numpy as np
# from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # define range of red color in HSV
    lower_red = np.array([17, 15, 100], dtype=np.uint8)
    upper_red = np.array([50, 56, 200], dtype=np.uint8)

    lower_green = np.array([6, 86, 29], dtype=np.uint8)
    upper_green = np.array([255, 255, 80], dtype=np.uint8)

    # Threshold the BGR image to get only red and green colors
    mask_red = cv2.inRange(frame, lower_red, upper_red)
    mask_green = cv2.inRange(frame, lower_green, upper_green)

    # Bitwise-AND mask and original image
    res_red = cv2.bitwise_and(frame,frame, mask= mask_red)
    res_green = cv2.bitwise_and(frame,frame, mask= mask_green)

    cv2.imshow('frame',frame)
    # cv2.imshow('mask',mask_red)
    cv2.imshow('res_red',res_red)
    cv2.imshow('res_green', res_green)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()