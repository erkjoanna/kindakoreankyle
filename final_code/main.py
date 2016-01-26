import sys
from signal import *
from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro, Motor, Color
from constants import *
from threading import Thread
from vision import *
from ir_sensor_helpers import *

camera = None
our_color = RED
most_recent_angle = 0
most_recent_distance = 0

def vision_thread(camera):
    global our_color
    global most_recent_angle
    global most_recent_distance

    while True:
       most_recent_angle, most_recent_distance = vision(camera, our_color)
       print most_recent_angle, most_recent_distance

def set_end(*args):
    if camera:
        cleanup_vision(camera)
    sys.exit(0)

class Movement (SyncedSketch):

    global our_color
    global most_recent_angle
    global most_recent_distance

    def setup(self):
        #setting up the gyro and two motors
        self.gyro = Gyro(self.tamp, GYRO, integrate = True)
        self.motor1 = Motor(self.tamp, DIR1, PWM1)
        self.motor2 = Motor(self.tamp, DIR2, PWM2)

        #initializing angle and distance
        self.angle = 0
        self.distance = 0

        #setting motor orientations (for fun)
        self.motor1.write(1,0) #1 is forward for Motor 1
        self.motor2.write(0,0) #0 is forward for Motor 2

        self.gyro_timer = Timer() #setting the timer for turning

        #setting up ir sensors
        self.short0 = AnalogInput(self.tamp, SHORT0)
        self.short1 = AnalogInput(self.tamp, SHORT1)
        self.short2 = AnalogInput(self.tamp, SHORT2)
        self.short3 = AnalogInput(self.tamp, SHORT3)
        self.short4 = AnalogInput(self.tamp, SHORT4)
        self.short5 = AnalogInput(self.tamp, SHORT5)
        self.long0 = AnalogInput(self.tamp, LONG0)
        self.long1 = AnalogInput(self.tamp, LONG1)
        self.long2 = AnalogInput(self.tamp, LONG2)
        self.long3 = AnalogInput(self.tamp, LONG3)
        self.long4 = AnalogInput(self.tamp, LONG4)
        self.long5 = AnalogInput(self.tamp, LONG5)

        # Initializing list to hold IR sensors
        self.ir_sensors = []
        self.ir_sensors.append((self.short0, self.long0))
        self.ir_sensors.append((self.short1, self.long1))
        self.ir_sensors.append((self.short2, self.long2))
        self.ir_sensors.append((self.short3, self.long3))
        self.ir_sensors.append((self.short4, self.long4))
        self.ir_sensors.append((self.short5, self.long5))

        self.ir_readings = [(0,0)] * 6 # readings are formatted as (short, long)

        self.main_timer = Timer() # setting the timer for wall avoidance

        #setting up the color sensor
        self.color = Color(self.tamp, integrationTime=Color.INTEGRATION_TIME_101MS, gain=Color.GAIN_1X)

        #robot movement variables
        self.state = CALCULATING
        self.stuck = NOT_STUCK
        self.starting_angle = self.gyro.val     
        
        #flapper variables
        self.detected_color = NOBLOCK
        self.color_count = 0
        self.desired_color_count = 2 #want to read consecutive readings to ascertain color

    def loop(self):

        IR Sensor Readings
        if self.main_timer.millis() > 100:

            self.main_timer.reset()

            # Color sorting blocks
            self.color_sorting()

            # Check IR Sensors
            self.check_ir_sensors()

        
        if self.state == CALCULATING:

            ###VISION###
            angle = most_recent_angle
            distance = most_recent_distance

            # Vision does not see any color, rotate in place.
            if angle == None and distance == None:
                self.angle = 360

            self.starting_angle = self.gyro.val
            self.state = TURNING

            ###ENCODERS###

        elif self.state == TURNING:

            if (self.stuck == STUCK):

                # Rotate if stuck until we're out of UNSTUCK state.
                self.angle = 90

                self.motor1.write(0, 10)
                self.motor2.write(0, 10)

            else:

                #take a snapshot of the current gyro number

                #while the robot hasn't turned desired degrees yet
                if self.gyro_timer.millis()>100:
                    #print "starting_angle: ", self.starting_angle #check.
                    print "difference: ",(self.gyro.val)-self.starting_angle
                    self.gyro_timer.reset()
                    if self.angle > 0:
                        self.motor1.write(0,10)
                        self.motor2.write(0,10)
                        if ((self.gyro.val) - self.starting_angle) > self.angle:
                            self.state = MOVING        
                    elif self.angle < 0:
                        self.motor1.write(1,10)
                        self.motor2.write(1,10)
                        if ((self.gyro.val) - self.starting_angle) < self.angle:
                            self.state = MOVING
                    else:
                        self.state = MOVING

        elif self.state == MOVING:
            #move the robot forward for a second - THIS DOESN'T QUITE WORK YET
            self.motor1.write(1,10)
            self.motor2.write(0,10) 
            
            if self.gyro_timer.millis() > 3000:            
                self.state = CALCULATING
                self.gyro_timer.reset()


    def color_sorting(self):
        if (self.color.r > 1.3 * self.color.g and self.color.r > 1.3 * self.color.b):
            if self.detected_color == RED:
                self.count = self.count + 1
            else:
                self.detected_color = RED
                self.count = 0
        elif (self.color.g > 1.3 * self.color.r and self.color.g > 1.3 * self.color.b):
            if self.detected_color == GREEN:
                self.count = self.count + 1
            else:
                self.detected_color = GREEN
                self.count = 0

        if not self.detected_color == NOBLOCK and self.count > 5:
            #decide the appropriate place to move slapper
            print "color is", self.detected_color
            self.detected_color = NOBLOCK
            self.count = 0

    def check_ir_sensors(self):
        # Get the sensor readings and find the distances
        for i in xrange(len(self.ir_readings)):
            short_ir_reading = self.ir_sensors[i][0].val / 1000.0
            long_ir_reading = self.ir_sensors[i][1].val / 1000.0

            self.ir_readings[i] = voltage_to_distance(short_ir_reading, long_ir_reading)

        sensors_too_close = []

        # Check if the robot is too close to the walls.
        for i in xrange(len(self.ir_readings)):
            short_ir, long_ir = self.ir_readings[i]

            if (short_ir < THRESHOLD or long_ir < THRESHOLD):
                sensors_too_close.append(i)

        # It is stuck if sensors 0, 1, 2 or 0, 4, 5 are < THRESHOLD

        too_close_count_1 = 0
        for i in [i in sensors_too_close for i in STUCK_SENSORS_1]:
            if i:
                too_close_count_1 += 1

        too_close_count_2 = 0
        for i in [i in sensors_too_close for i in STUCK_SENSORS_2]:
            if i:
                too_close_count_2 += 1

        # Stuck! (Robot is too close to walls and vision sees no color.)
        if (too_close_count_1 >= 3 or too_close_count_2 >= 3) and self.angle == None:
            self.stuck == STUCK
            self.state = TURNING

        else:
            self.stuck == UNSTUCK

if __name__ == "__main__":

    camera = setup_vision()
    
    thread_vision = Thread( target=vision_thread, args=(camera,))
    thread_vision.daemon = True
    thread_vision.start()

    sketch = Movement(3,-0.00001, 100)
    sketch.run()
   
    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, set_end)
    
    time.sleep(10000)
