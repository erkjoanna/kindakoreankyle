import cv2
import numpy as np
import scipy.misc
import time 
import math

def floodfill(matrix, x, y):
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a".
    if matrix[x][y] == "a":  
        matrix[x][y] = "c" 
        #recursively invoke flood fill on all surrounding cells:
        if x > 0:
            floodfill(matrix,x-1,y)
        if x < len(matrix[y]) - 1:
            floodfill(matrix,x+1,y)
        if y > 0:
            floodfill(matrix,x,y-1)
        if y < len(matrix) - 1:
            floodfill(matrix,x,y+1)

def calculate_average(src, x, y, sum_x, sum_y, total):

	sum_total = summation(src, x, y, sum_x, sum_y, total)

	final_x = float(sum_total[0])/sum_total[2]
	final_y = float(sum_total[1])/sum_total[2]

	return final_x, final_y


def summation(src, x, y, sum_x, sum_y, total):

	if src[y][x][2] > 168:
		sum_x += x
		sum_y += y
		total += 1
		print x, y, total
		src[y][x] = np.array([0, 0, 0], dtype=np.uint8)

		if x > 0: # search left
			sum_x, sum_y, total = summation(src, x-1, y, sum_x, sum_y, total)
		if x < src.shape[1] - 1: # search right
			sum_x, sum_y, total = summation(src, x+1, y, sum_x, sum_y, total)
		if y > 0:
			sum_x, sum_y, total = summation(src, x, y-1, sum_x, sum_y, total)
		if y < src.shape[0] - 1:
			sum_x, sum_y, total = summation(src, x, y+1, sum_x, sum_y, total)

	
	return sum_x, sum_y, total

# Captures a single image from the camera and returns it in PIL format
def get_image():
	# read is the easiest way to get a full image out of a VideoCapture object.
	retval, im = camera.read()
	return im

img = cv2.imread("red_image_with_green_averages.png")
img_w = img.shape[1]
img_h = img.shape[0]

middle_w = img_w/2.0
k = .01 # each pixel is about .01 inches

for x in xrange(img_w):
	for y in xrange(img_h):
		# Green pixel found
		if (img[y][x][0] == 0 and img[y][x][1] == 255 and img[y][x][2] == 0):
			print "x coordinate", x, "y coordinate", y
			print "middle width", middle_w
			# Get x coordinate of the pixel
			# Compare it to middle_w
			difference = middle_w - x
			print "difference", difference
			actual_x = abs(difference)
			actual_y = img_h - y

			distance = math.hypot(actual_x, actual_y)*k

			if difference > 0:
				# LEFTSIDE
				angle = - math.atan(float(actual_x)/actual_y) * 180.0 / math.pi
			else:
				# RIGHTSIDE
				angle = math.atan(float(actual_x)/actual_y) * 180.0 / math.pi

			print "angle", angle, "degrees", "distance", distance, "inches"