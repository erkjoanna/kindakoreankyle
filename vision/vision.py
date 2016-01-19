import cv2
import numpy as np
import scipy.misc
import time 

# Camera 0 is the integrated web cam on my netbook
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
camera = cv2.VideoCapture(camera_port)

'''
Params:
src - the source image
x - x-coordinate of the pixel of color object
y - y-coordinate of the pixel of color object

Returns:
the average of all the pixels the color object is composed of
'''
def calculate_average(src, x, y):

	sum_total = summation(src, x, y, 0, 0, 0)

	final_x = float(sum_total[0])/sum_total[2]
	final_y = float(sum_total[1])/sum_total[2]

	return final_x, final_y


'''
Params:
src - the source image
x - x-coordinate of the pixel of color object
y - y-coordinate of the pixel of color object
sum_x - running sum of the x-coordinates of the color object
sum_y - running sum of the y-coordinates of the color object
total - running sum of the number of pixels of the color object

Returns:
sum_x - running sum of the x-coordinates of the color object
sum_y - running sum of the y-coordinates of the color object
total - running sum of the number of pixels of the color object
'''
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

'''
Returns the image read from the camera
'''
def get_image():
	retval, im = camera.read()
	return im
 
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
for i in xrange(ramp_frames):
	temp = get_image()


print "Taking pictures..."

# while(1):

# Take the actual image we want to keep
camera_capture = get_image()

# Scale down the image by 1/4
img = scipy.misc.imresize(camera_capture, 0.25)

# Image width and height
img_w = img.shape[1]
img_h = img.shape[0]

cv2.imwrite("orig_img.png", img)

# TODO: Better detection of the range of values for red and green
# Define range of red color in HSV
lower_red = np.array([17, 15, 100], dtype=np.uint8)
upper_red = np.array([50, 56, 200], dtype=np.uint8)

lower_green = np.array([6, 86, 29], dtype=np.uint8)
upper_green = np.array([255, 255, 80], dtype=np.uint8)

# Threshold the BGR image to get only red and green colors
mask_red = cv2.inRange(img, lower_red, upper_red)
mask_green = cv2.inRange(img, lower_green, upper_green)

# Bitwise-AND mask and original image
res_red = cv2.bitwise_and(img, img, mask= mask_red)
res_green = cv2.bitwise_and(img, img, mask= mask_green)

print "Writing red image..."
cv2.imwrite("mask_red2.png", mask_red)
print mask_red, mask_red.shape, mask_red.dtype
cv2.imwrite("red_image2.png", res_red)

res_red2 = cv2.imread("red_image2.png")

# Loop through each pixel of the red result and check if there is a red pixel
for x in xrange(img_w):
	for y in xrange(img_h):

		if res_red2[y][x][2] > 168: # TODO: improve better detection of red.
			print "coordinates that are red", x, y

			# Run 'Flood Fill' to find the average of the blob it incapsulates.
			avg_x, avg_y = calculate_average(res_red2, x, y)
			res_red2[avg_y][avg_x] = np.array([0, 255, 0], dtype=np.uint8)
			print "Average", avg_x, avg_y

print "Writing red image with averages..."
cv2.imwrite("red_image_with_green_averages2.png", res_red2)

# time.sleep(5)
 
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(camera)