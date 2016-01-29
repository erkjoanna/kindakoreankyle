###################COLORS#####################
NOBLOCK = -1
RED = 0
GREEN = 1

###################STATES#####################
CALCULATING = 0
TURNING = 1
MOVING  = 2
BACKING_OFF = 3

###################STUCK#####################
NOT_STUCK = 0
STUCK = 1
STUCK_SENSORS_1 = [0, 1, 2]
STUCK_SENSORS_2 = [4, 5, 6]

####################PINS######################
#----------------IR SENSORS------------------#
# Clockwise every 60 degrees from the front
LONG0 = 22 
SHORT0 = 27 #23 
LONG1 = 16 
SHORT1 = 17 
LONG2 = 14
SHORT2 = 15
LONG3 = 28
# SHORT3 = 27
LONG4 = 37 #A13
SHORT4 = 36 #A12
LONG5 = 35 #A11
SHORT5 = 34 #A10
THRESHOLD = 8

#---------WHEEL MOTORS AND ENCODER-----------#
DIR1 = 2
PWM1 = 3
EN01 = 0
EN11 = 1

DIR2 = 7
PWM2 = 6
EN02 = 8
EN12 = 9

DIR6 = 31
PWM6 = 32
EN06 = 33
EN16 = 26

#---------------BRUSH MOTORS------------------#
DIR3 = 21
PWM3 = 4
DIR5 = 22
PWM5 = 5


#-------------OTHER DEVICES------------------#
GYRO = 10 #chip select
#GYRO_IN = 11  #MOSI
#GYRO_OUT = 12 #MISO
#COLOR_SENSOR_SCL = 19 #these are already defined in original adafruit library because only 1 pair of scl/sda channels
#COLOR_SENSOR_SDA = 18
COLOR_LED = 24
START_PIN = 25

PWM7 = 21 # Servo PWM for Red
PWM8 = 20 # Servo PWM for Green

####################VISION######################
COMPUTER_CAM = 0
WEB_CAM = 1
RAMP_FRAMES = 30
COLOR_CHECK_RED = 1.3
COLOR_CHECK_GREEN = 1.1
BLOB_MIN_SIZE = 1000
PIXEL_TO_CENTIMETERS = 0.06
BLOB_SCALE_FACTOR = 500.0

############ COLOR SENSORS / BSLAPPER ###########
RED_THRESH = 1.3
GREEN_THRESH = 1.2
CONSISTENCY_THRESH = 2
SLAPPER_SPEED = 80

################OTHER###################
TURN_MILLIS = 10000
TURN_SPEED = 17
FORWARD_SPEED = 22
FORWARD_THRESHOLD = 5




