###################SWITCHES#####################
# START = 
# GAME_COLOR = 

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
LONG0 = 22 
SHORT0 = 23 
LONG1 = 16 
SHORT1 = 17 
LONG2 = 14
SHORT2 = 15
LONG3 = 28
SHORT3 = 27
LONG4 = 13 #A13
SHORT4 = 12 #A12
LONG5 = 11 #A11
SHORT5 = 10 #A10
THRESHOLD = 8 #Centimeters

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
PWM6 = 23
EN06 = 30
EN16 = 29

#-------------OTHER DEVICES------------------#
GYRO = 10 #chip select
#GYRO_IN = 11  #MOSI
#GYRO_OUT = 12 #MISO
#COLOR_SENSOR_SCL = 19 #these are already defined in original adafruit library because only 1 pair of scl/sda channels
#COLOR_SENSOR_SDA = 18

PWM7 = 21 # Servo PWM for Red
PWM8 = 20 # Servo PWM for Green

####################VISION######################
#---------------CAMERA PORT-----------------#
COMPUTER_CAM = 0
WEB_CAM = 1
RAMP_FRAMES = 30
COLOR_CHECK = 1.1


