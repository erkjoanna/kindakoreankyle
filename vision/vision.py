import cv2
import numpy as np
import scipy.misc
import time 

# Camera 0 is the integrated web cam on my netbook
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
 

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
 
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
for i in xrange(ramp_frames):
	temp = get_image()

print("Taking image...")

while(1):

	# Take the actual image we want to keep
	camera_capture = get_image()
	# file = "test_image.png"
	# # A nice feature of the imwrite method is that it will automatically choose the
	# # correct format based on the file extension you provide. Convenient!
	# cv2.imwrite(file, camera_capture)

	img = scipy.misc.imresize(camera_capture, 0.25)
	img_w = img.shape[1]
	img_h = img.shape[0]

	# define range of red color in HSV
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
	cv2.imwrite("red_image.png", res_red)

	res_red2 = cv2.imread("red_image.png")

	for x in xrange(img_w):
		for y in xrange(img_h):

			if res_red2[y][x][2] > 168: # red pixel ==> object exists!
				print "coordinates that are red", x, y
				# Run 'Flood Fill' to find the average of the blob it incapsulates.
				avg_x, avg_y = calculate_average(res_red2, x, y, 0, 0, 0)
				res_red2[avg_y][avg_x] = np.array([0, 255, 0], dtype=np.uint8)
				print "Average", avg_x, avg_y

	print "Writing red image with averages..."
	cv2.imwrite("red_image_with_green_averages.png", res_red2)

	time.sleep(5)
 
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(camera)