import cv2
import numpy as np
import scipy.misc
import time, math
from Queue import *


camera_port = 1
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
camera = cv2.VideoCapture(camera_port)

'''
Params:
src - the source image
x - x-coordinate of the pixel of color object
y - y-coordinate of the pixel of color object

Returns:
avg_x - the average x-coordinate of all the pixels in the color object
avg_y - the average y-coordinate of all the pixels in the color object
total - the total number of pixels in the color object
'''
def calculate_average(src, x, y):

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
			if check_neighbor(src, current_x-1, current_y):
				q.put((current_x-1, current_y))
		if current_x < src.shape[1] - 1: # search right
			if check_neighbor(src, current_x+1, current_y):
				q.put((current_x+1, current_y))

		if current_y > 0:
			if check_neighbor(src, current_x, current_y-1):
				q.put((current_x, current_y-1))

		if current_y < src.shape[0] - 1:
			if check_neighbor(src, current_x, current_y+1):
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

Returns:
True if the neighboring pixel is a red pixel, otherwise False
'''
def check_neighbor(src, x, y):
	r = src[y][x][2]
	g = src[y][x][1]
	b = src[y][x][0]

	if (r > 1.3 * g) and (r > 1.3 * b):
		src[y][x] = np.array([0, 0, 0], dtype=np.uint8)

		return True
	
	return False


'''
Returns the image read from the camera
'''
def get_image():
	retval, im = camera.read()
	return im
 

'''
Params:
src - the source image
x - x-coordinate of the pixel of color object
y - y-coordinate of the pixel of color object

Returns:
avg_x - the average x-coordinate of all the pixels in the color object
avg_y - the average y-coordinate of all the pixels in the color object
total - the total number of pixels in the color object
'''
def vision(color):


	# Ramp the camera - these frames will be discarded and are only used to allow v4l2
	# to adjust light levels, if necessary
	for i in xrange(ramp_frames):
		temp = get_image()



	# Take the actual image we want to keep
	camera_capture = get_image()

	img = scipy.misc.imresize(camera_capture, 0.25)
	img_w = img.shape[1]
	img_h = img.shape[0]

	cv2.imwrite("orig_img.png", img)

	# Creating mask
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

	cv2.imwrite("mask_2.png", mask)

	print "Creating resulting red only picture..."

res_red = cv2.bitwise_and(img, img, mask= mask)

cv2.imwrite("red_2.png", res_red)

print "Flood fill to find average..."

img2 = np.copy(res_red)

largest_blob = 0
final_avg_x = 0
final_avg_y = 0

# Loop through each pixel of the red result and check if there is a red pixel
for x in xrange(img_w):
	for y in xrange(img_h):

		r = img2[y][x][2]
		g = img2[y][x][1]
		b = img2[y][x][0]

		if (r > 1.3 * g) and (r > 1.3 * b):

			# Run 'Flood Fill' to find the average of the blob it incapsulates.
			avg_x, avg_y, total = calculate_average(img2, x, y)

			if (total > largest_blob):
				largest_blob = total
				final_avg_x = avg_x
				final_avg_y = avg_y

img2[final_avg_y][final_avg_x] = np.array([0, 255, 0], dtype=np.uint8)

print "Writing red image with averages..."
cv2.imwrite("red_avg_2.png", img2)


print "Finding angle and distance..."

img = cv2.imread("red_avg_2.png")
img_w = img.shape[1]
img_h = img.shape[0]

middle_w = img_w/2.0
k = .01 # each pixel is about .01 inches

for x in xrange(img_w):
	for y in xrange(img_h):
		# Green pixel found
		if (img[y][x][0] == 0 and img[y][x][1] == 255 and img[y][x][2] == 0):
			# Get x coordinate of the pixel
			# Compare it to middle_w
			difference = middle_w - x
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
