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
STUCK_SENSORS_2 = [0, 4, 5]

####################PINS######################
#----------------IR SENSORS------------------#
# Clockwise every 60 degrees from the front
LONG0 = 10 #A10
SHORT0 = 11 #A11
LONG1 = 12 #A12
SHORT1 = 13 #A13
LONG2 = 27
SHORT2 = 28
LONG3 = 23
SHORT3 = 22
LONG4 = 17
SHORT4 = 16
LONG5 = 15
SHORT5 = 14
THRESHOLD = 5

#---------------WHEEL MOTORS-----------------#
DIR1 = 2
PWM1 = 3
PWM2 = 6
DIR2 = 7

#---------------SLAPPER MOTORS-----------------#
DIR6 = 31
PWM6 = 32

#-------------OTHER DEVICES------------------#
GYRO = 10 #chip select
#GYRO_IN = 11  #MOSI
#GYRO_OUT = 12 #MISO
#COLOR_SENSOR_SCL = 19 #these are already defined in original adafruit library because only 1 pair of scl/sda channels
#COLOR_SENSOR_SDA = 18

####################VISION######################
#---------------CAMERA PORT-----------------#
COMPUTER_CAM = 0
WEB_CAM = 1
RAMP_FRAMES = 30
COLOR_CHECK = 1.1


