import sys
from signal import *
from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro, Motor, Color, Encoder, AnalogInput, Servo
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
       print "hi"
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
        self.encoder1 = Encoder(self.tamp, EN01, EN11, continuous=True)
        self.encoder2 = Encoder(self.tamp, EN02, EN12, continuous=True)
        self.encoder6 = Encoder(self.tamp, EN06, EN16, continuous=True)

        # Wheel Motors
        self.motor1 = Motor(self.tamp, DIR1, PWM1)
        self.motor2 = Motor(self.tamp, DIR2, PWM2)

        # Brush Motors
        self.motor3 = Motor(self.tamp, 21, 4)
        self.motor5 = Motor(self.tamp, 22, 5)

        # Slapper
        self.motor6 = Motor(self.tamp, DIR6, PWM6)

        #initializing angle and distance
        self.angle = 0
        self.distance = 0

        #setting motor orientations (for fun)
        self.motor1.write(1,0) #1 is forward for Motor 1
        self.motor2.write(0,0) #0 is forward for Motor 2

        # self.motor3.write(0,75)
        # self.motor5.write(0,75)

        # #setting up ir sensors
        self.short0 = AnalogInput(self.tamp, SHORT0)
        self.short1 = AnalogInput(self.tamp, SHORT1)
        self.short2 = AnalogInput(self.tamp, SHORT2)
        self.short3 = AnalogInput(self.tamp, SHORT0)
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
        self.ir_sensors.append(self.short0)
        self.ir_sensors.append(self.long1)
        self.ir_sensors.append(self.long2)
        self.ir_sensors.append(self.short3)
        self.ir_sensors.append(self.short4)
        self.ir_sensors.append(self.short5)
        self.ir_sensors.append(self.long0)


        self.ir_readings = [0] * 6 # readings are formatted as (short, long)

        self.ir_count = 0

        self.main_timer = Timer() # setting the timer for wall avoidance
        self.gyro_timer = Timer() # setting the timer for turning
        self.game_timer = Timer() # setting the timer for the servo

        # setting up the servos
        self.green_servo = Servo(self.tamp, PWM7)
        self.red_servo = Servo(self.tamp, PWM8)
        self.servos = [self.red_servo, self.green_servo]

        #setting up the color sensor
        # self.color = Color(self.tamp, integrationTime=Color.INTEGRATION_TIME_101MS, gain=Color.GAIN_1X)

        #robot movement variables
        self.state = CALCULATING
        self.stuck = NOT_STUCK
        self.starting_angle = self.gyro.val     
        
        #flapper variables
        self.detected_color = NOBLOCK
        self.color_count = 0
        self.desired_color_count = 2 #want to read consecutive readings to ascertain color

        self.finding = False

    def loop(self):

        # After 3 minutes
        if self.game_timer.millis() > 179000:

            print "Game Over!"
            self.servos[our_color].write(1050)


        if self.main_timer.millis() > 100:

            self.main_timer.reset()

            # Color sorting blocks
            # self.color_sorting()

            # Check IR Sensors
            if self.game_timer.millis() > 500:

                self.check_ir_sensors()

        
        if self.state == CALCULATING:
            # print "CALCULATING"

            ###VISION###
            angle = most_recent_angle
            distance = most_recent_distance

            # Vision does not see any color, rotate in place.
            if angle == None and distance == None:
                self.angle = 360
                self.finding = True

            self.starting_angle = self.gyro.val
            self.state = TURNING

            ###ENCODERS###

        elif self.state == TURNING:
            # print "TURNING"

            if (self.stuck == STUCK):

                # Rotate if stuck until we're out of UNSTUCK state.
                # print "TURNING STUCK"
                self.angle = 90

                self.motor1.write(0, 20)
                self.motor2.write(0, 20)

            else:
                # print "TURNING NOT STUCK"
                #take a snapshot of the current gyro number

                #while the robot hasn't turned desired degrees yet
                if self.gyro_timer.millis()>100:
                    #print "starting_angle: ", self.starting_angle #check.
                    # print "difference: ",(self.gyro.val)-self.starting_angle
                    self.gyro_timer.reset()
                    if self.angle > 0:
                        self.motor1.write(0,30)
                        self.motor2.write(0,30)
                        if self.finding and most_recent_angle:
                            self.state = CALCULATING
                            return
                        if ((self.gyro.val) - self.starting_angle) > self.angle:
                            self.state = MOVING        
                    elif self.angle < 0:
                        self.motor1.write(1,30)
                        self.motor2.write(1,30)
                        if self.finding and most_recent_angle:
                            self.state = CALCULATING
                            return
                        if ((self.gyro.val) - self.starting_angle) < self.angle:
                            self.state = MOVING
                    else:
                        self.state = MOVING

        elif self.state == MOVING:

            # print "MOVING"
            #move the robot forward for a second - THIS DOESN'T QUITE WORK YET
            self.motor1.write(0,25)
            self.motor2.write(1,25) 
            
            if self.gyro_timer.millis() > 3000:            
                self.state = CALCULATING
                self.gyro_timer.reset()


    def color_sorting(self):
        if (self.color.r > 1.3 * self.color.g and self.color.r > 1.3 * self.color.b):
            if self.detected_color == RED:
                self.color_count = self.color_count + 1
            else:
                self.detected_color = RED
                self.color_count = 0
        elif (self.color.g > COLOR_CHECK * self.color.r and self.color.g > COLOR_CHECK * self.color.b):
            if self.detected_color == GREEN:
                self.color_count = self.color_count + 1
            else:
                self.detected_color = GREEN
                self.color_count = 0

        if not self.detected_color == NOBLOCK and self.color_count > 5:
            #decide the appropriate place to move slapper
            print "color is", self.detected_color
            self.motor6.write(self.detected_color, 20)
            encoder_initial = self.encoder6.val
            sign = 1-2*self.detected_color
            # while (sign*(self.encoder6.val - encoder_initial) < 3200):
                # continue
            self.motor6.write(self.detected_color,0)
            self.detected_color = NOBLOCK
            self.color_count = 0

    def check_ir_sensors(self):
        # Get the sensor readings and find the distances

        for i in xrange(len(self.ir_readings)):
            ir_reading = self.ir_sensors[i].val / 1000.0

            self.ir_readings[i] = short_ir_distance(ir_reading)


        sensors_too_close = []

        # Check if the robot is too close to the walls.
        for i in xrange(len(self.ir_readings)):
            ir = self.ir_readings[i]

            if (ir < THRESHOLD):


                sensors_too_close.append(i)


        # It is stuck if sensors 0, 1, 2 or 4, 5, 6 are < THRESHOLD


        # See if the sensors that are too close are 0, 1, 2 or 0, 4, 5.
        too_close_count_1 = 0
        too_close_count_2 = 0

        for i in sensors_too_close:
            if (i in STUCK_SENSORS_1):
                too_close_count_1 += 1

            if (i in STUCK_SENSORS_2):
                too_close_count_2 += 1

        # Stuck! (Robot is too close to walls and vision sees no color.)
        if (too_close_count_1 >= 3 or too_close_count_2 >= 3):
            # TODO: and self.angle == None ^^^^

            # Make sure we get a stuck reading 3 times before we declare it stuck.
            self.ir_count += 1

            if self.ir_count >= 5:

                # Stuck, and turning now. Reset the reading count.
                self.stuck = STUCK
                self.state = TURNING
                self.ir_count = 0
        else:
            self.ir_count = 0
            self.stuck = NOT_STUCK
            # print "NOT STUCK"
            self.state = CALCULATING
            # print "STATE", self.state, "STUCK?", self.stuck
            # self.state = MOVING


        # print self.ir_count
        # print "STATE", self.state, "STUCK?", self.stuck


            # else:
            #     self.stuck = NOT_STUCK
            #     print "STATE", self.state, "STUCK?", self.stuck


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
