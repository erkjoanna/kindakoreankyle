import cv2
import numpy as np
import time, math
import scipy.misc
from Queue import *
from constants import *

###################### SETUP / CLEANUP ###########################
'''
Function that finds out what port the webcam is connected to
'''
def findPort():
	port = 0
	isFunctional = False

	while not isFunctional:
		port = port + 1
		camera = cv2.VideoCapture(port)
		isFunctional, temp = camera.read()

	print port
	return port


'''
Function that sets up webcam

Returns:
camera - the camera that will take pictures
'''
def setup_vision():
	camera = cv2.VideoCapture(findPort())
	return camera


'''
Function that cleans up camera

Params:
camera - camera acquired to be released
'''
def cleanup_vision(camera):
	camera.release()


####################### ACTUAL VISION CODE ###########################
'''
Params:
src - the source image
x - x-coordinate of the pixel of color object
y - y-coordinate of the pixel of color object
color - color of the game

Returns:
avg_x - the average x-coordinate of all the pixels in the color object
avg_y - the average y-coordinate of all the pixels in the color object
total - the total number of pixels in the color object
'''
def calculate_average(src, x, y, color):

	total_x = 0
	total_y = 0
	total = 0

	q = Queue()
	q.put((x, y))

	while (not q.empty()):

		(current_x, current_y) = q.get()

		# Add this x, y to the running sum
		total_x += current_x
		total_y += current_y
		total += 1

		if current_x > 0: # search left
			if check_neighbor(src, current_x-1, current_y, color):
				q.put((current_x-1, current_y))
		if current_x < src.shape[1] - 1: # search right
			if check_neighbor(src, current_x+1, current_y, color):
				q.put((current_x+1, current_y))

		if current_y > 0:
			if check_neighbor(src, current_x, current_y-1, color):
				q.put((current_x, current_y-1))

		if current_y < src.shape[0] - 1:
			if check_neighbor(src, current_x, current_y+1, color):
				q.put((current_x, current_y+1))

	# Take average
	avg_x = float(total_x)/total
	avg_y = float(total_y)/total

	return avg_x, avg_y, total


'''
Params:
src - the source image
x - x-coordinate of the pixel of color object
y - y-coordinate of the pixel of color object
color - color of the game

Returns:
True if the neighboring pixel is a red pixel, otherwise False
'''
def check_neighbor(src, x, y, color):

	if check_game_color(src, x, y, color):
		src[y][x] = np.array([0, 0, 0], dtype=np.uint8)

		return True
	
	return False

'''
Params:
img - the source image
x - x-coordinate of pixel
y - y-coordinate of pixel
color - boolean, RED(0) or GREEN(1)

Returns:
True if pixel color is the color, else False
'''
def check_game_color(img, x, y, color):
	if color == RED:
		C = COLOR_CHECK_RED
	elif color == GREEN:
		C = COLOR_CHECK_GREEN

	return img[y][x][2-color] > C * img[y][x][0] and img[y][x][2-color] > C * img[y][x][1+color]


'''
Function that tells the robot what angle to turn at and the distance
it should move at.

Params:
camera - camera aquired
color - boolean, RED(0) or GREEN(1)

Returns:
angle - the angle the robot to turn at. Middle is 0 degrees. 
		Angles to the right are positive and Angles to the left are negative.
distance - the distance the robot should move forward.
'''
def vision(camera, color):
	time.sleep(1)
    
	# Take the actual image we want to keep
	_, camera_capture = camera.read()


	img = scipy.misc.imresize(camera_capture, 0.25)
	cv2.imwrite("orig_img2.png", img)

	img_w = img.shape[1]
	img_h = img.shape[0]

	largest_blob = 0
	final_avg_x = None
	final_avg_y = None

	pixelskip = 4 #constant we tune, we skip to the nth next pixel
	for fractionx in xrange(img_w/pixelskip):
		for fractiony in xrange(img_h/pixelskip):
			x = fractionx * pixelskip
			y = fractiony * pixelskip
			if check_game_color(img, x, y, color):
				avg_x, avg_y, total = calculate_average(img, x, y, color)

				if (total > largest_blob):
					largest_blob = total
					final_avg_x = avg_x
					final_avg_y = avg_y
			else:
				img[y][x] = np.array([0, 0, 0], dtype=np.uint8)

	if (final_avg_x == None and final_avg_y == None) or largest_blob < BLOB_MIN_SIZE:
		return (None, None)

	img[final_avg_y][final_avg_x] = np.array([0, 0, 255], dtype=np.uint8)

	cv2.imwrite("img_with_average2.png", img)

	# Calculating angle and distance

	middle_w = img_w/2.0

	difference = middle_w - final_avg_x
	actual_x = abs(difference)
	actual_y = img_h - final_avg_y

	distance = math.hypot(actual_x, actual_y) * PIXEL_TO_CENTIMETERS * (BLOB_SCALE_FACTOR / largest_blob)

	if difference > 0:
		# LEFTSIDE
		angle = - (math.atan(float(actual_x)/actual_y) * 180.0 / math.pi) * (BLOB_SCALE_FACTOR / largest_blob)

	else:
		# RIGHTSIDE
		angle = math.atan(float(actual_x)/actual_y) * 180.0 / math.pi * (BLOB_SCALE_FACTOR / largest_blob)

	print "angle", angle, "degrees", "distance", distance, "centimeters"

	return (angle, distance)
