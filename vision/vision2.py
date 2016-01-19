import cv2
import numpy as np
import scipy.misc
import time 
import math

# img = cv2.imread("red_image_with_green_averages.png")
# img_w = img.shape[1]
# img_h = img.shape[0]

# middle_w = img_w/2.0
# k = .01 # each pixel is about .01 inches

# for x in xrange(img_w):
# 	for y in xrange(img_h):
# 		# Green pixel found
# 		if (img[y][x][0] == 0 and img[y][x][1] == 255 and img[y][x][2] == 0):
# 			print "x coordinate", x, "y coordinate", y
# 			print "middle width", middle_w
# 			# Get x coordinate of the pixel
# 			# Compare it to middle_w
# 			difference = middle_w - x
# 			print "difference", difference
# 			actual_x = abs(difference)
# 			actual_y = img_h - y

# 			distance = math.hypot(actual_x, actual_y)*k

# 			if difference > 0:
# 				# LEFTSIDE
# 				angle = - math.atan(float(actual_x)/actual_y) * 180.0 / math.pi
# 			else:
# 				# RIGHTSIDE
# 				angle = math.atan(float(actual_x)/actual_y) * 180.0 / math.pi

# 			print "angle", angle, "degrees", "distance", distance, "inches"

img = cv2.imread("orig_img.png")
img_w = img.shape[1]
img_h = img.shape[0]

print "img", img

mask = np.zeros((img_h, img_w), dtype=np.uint8)

for x in xrange(img_w):
	for y in xrange(img_h):
		r = img[y][x][2]
		g = img[y][x][1]
		b = img[y][x][0]
		if (r > 1.3 * g and r > 1.3 * b):
			mask[y][x] = np.array([255], dtype=np.uint8)
		else:
			mask[y][x] = np.array([0], dtype=np.uint8)

print "mask", mask, mask.shape
cv2.imwrite("mask_produced.png", mask)

res_red = cv2.bitwise_and(img, img, mask= mask)

cv2.imwrite("res_red_produced.png", res_red)

