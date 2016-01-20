import cv2
import numpy as np
import scipy.misc
import time, math
from Queue import *

print cv2.__version__

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

'''
Params:
src - the source image
x - x-coordinate of the pixel of color object
y - y-coordinate of the pixel of color object

Returns:
the average of all the pixels the color object is composed of
'''
def calculate_average(src, x, y):

	total_x = 0
	total_y = 0
	total = 0

	q = Queue()
	q.put((x, y))

	while (not q.empty()):

		(current_x, current_y) = q.get()
		print current_x, current_y

		# Add this x, y to the running sum
		total_x += current_x
		total_y += current_y
		total += 1

		if current_x > 0: # search left
			if check_neighbor(src, current_x-1, current_y):
				q.put((current_x-1, current_y))
		if x < src.shape[1] - 1: # search right
			if check_neighbor(src, current_x+1, current_y):
				q.put((current_x+1, current_y))

		if y > 0:
			if check_neighbor(src, current_x, current_y-1):
				q.put((current_x, current_y-1))

		if y < src.shape[0] - 1:
			if check_neighbor(src, current_x, current_y+1):
				q.put((current_x, current_y+1))

	# Take average
	avg_x = float(total_x)/total
	avg_y = float(total_y)/total

	return avg_x, avg_y


def check_neighbor(src, x, y):
	r = src[y][x][2]
	g = src[y][x][1]
	b = src[y][x][0]

	if (r > 1.3 * g) and (r > 1.3 * b):
		src[y][x] = np.array([0, 0, 0], dtype=np.uint8)

		return True
	
	return False

# '''
# Params:
# src - the source image
# x - x-coordinate of the pixel of color object
# y - y-coordinate of the pixel of color object

# Returns:
# the average of all the pixels the color object is composed of
# '''
# def calculate_average(src, x, y):

# 	sum_total = summation(src, x, y, 0, 0, 0)

# 	print sum_total

# 	final_x = float(sum_total[0])/sum_total[2]
# 	final_y = float(sum_total[1])/sum_total[2]

# 	return final_x, final_y


# '''
# Params:
# src - the source image
# x - x-coordinate of the pixel of color object
# y - y-coordinate of the pixel of color object
# sum_x - running sum of the x-coordinates of the color object
# sum_y - running sum of the y-coordinates of the color object
# total - running sum of the number of pixels of the color object

# Returns:
# sum_x - running sum of the x-coordinates of the color object
# sum_y - running sum of the y-coordinates of the color object
# total - running sum of the number of pixels of the color object
# '''
# def summation(src, x, y, sum_x, sum_y, total):

# 	r = src[y][x][2]
# 	g = src[y][x][1]
# 	b = src[y][x][0]


# 	if r > 1.3*g and r > 1.3*b:
# 		sum_x += x
# 		sum_y += y
# 		total += 1
# 		src[y][x] = np.array([0, 0, 0], dtype=np.uint8)

# 		if x > 0: # search left
# 			sum_x, sum_y, total = summation(src, x-1, y, sum_x, sum_y, total)
# 		if x < src.shape[1] - 1: # search right
# 			sum_x, sum_y, total = summation(src, x+1, y, sum_x, sum_y, total)
# 		if y > 0:
# 			sum_x, sum_y, total = summation(src, x, y-1, sum_x, sum_y, total)
# 		if y < src.shape[0] - 1:
# 			sum_x, sum_y, total = summation(src, x, y+1, sum_x, sum_y, total)

	
# 	return sum_x, sum_y, total



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

cv2.imwrite("mask_2.png", mask)

res_red = cv2.bitwise_and(img, img, mask= mask)

cv2.imwrite("red_2.png", res_red)

img2 = np.copy(res_red)


# Loop through each pixel of the red result and check if there is a red pixel
for x in xrange(img_w):
	for y in xrange(img_h):

		r = img2[y][x][2]
		g = img2[y][x][1]
		b = img2[y][x][0]

		if r > 1.3*g and r > 1.3*b:
			print "coordinates that are red", x, y

			# Run 'Flood Fill' to find the average of the blob it incapsulates.
			avg_x, avg_y = calculate_average(img2, x, y)
			img2[avg_y][avg_x] = np.array([0, 255, 0], dtype=np.uint8)
			# print "Average", avg_x, avg_y

print "Writing red image with averages..."
cv2.imwrite("red_avg_2.png", img2)
