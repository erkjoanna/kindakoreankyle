import sys
from signal import *
from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro, Motor, Color, Encoder, AnalogInput, Servo, DigitalInput
from constants import *
from threading import Thread
from vision import *
from ir_sensor_helpers import *

camera = None
our_color = None
most_recent_angle = None
most_recent_distance = None

def vision_thread(camera):
    global our_color
    global most_recent_angle
    global most_recent_distance

    print our_color
    while True:
       most_recent_angle, most_recent_distance = vision(camera, our_color)
       # print most_recent_angle, most_recent_distance

def set_end(*args):
    if camera:
        cleanup_vision(camera)
    sys.exit(0)

class Movement (SyncedSketch):


    def setup(self):
        #setup color
        self.start = DigitalInput(self.tamp, START_PIN)
        self.color_led = DigitalInput(self.tamp, COLOR_LED)


        self.gyro = Gyro(self.tamp, GYRO, integrate = True)

        #setting up the gyro and three motors
        self.encoder1 = Encoder(self.tamp, EN01, EN11, continuous=True)
        self.encoder2 = Encoder(self.tamp, EN02, EN12, continuous=True)
        self.encoder6 = Encoder(self.tamp, EN06, EN16, continuous=True)

        # Wheel Motors
        self.motor1 = Motor(self.tamp, DIR1, PWM1)
        self.motor2 = Motor(self.tamp, DIR2, PWM2)
        self.motor6 = Motor(self.tamp, DIR6, PWM6)

        #initializing angle and distance
        self.angle = 0
        self.distance = 0
        self.farthest_sensor_angle = None

        # Brush Motors
        self.motor3 = Motor(self.tamp, DIR3, PWM3)
        self.motor5 = Motor(self.tamp, DIR5, PWM5)

        #setting up the color sensor
        self.color1 = Color(self.tamp, 0, integrationTime=Color.INTEGRATION_TIME_101MS, gain=Color.GAIN_1X)
        self.color2 = Color(self.tamp, 1, integrationTime=Color.INTEGRATION_TIME_101MS, gain=Color.GAIN_1X)

        #setting up ir sensors
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

        self.ir_readings = [0] * 7

        self.short_ir_sensors = []
        self.short_ir_sensors.append(self.short0)
        self.short_ir_sensors.append(self.long1)
        self.short_ir_sensors.append(self.long2)
        self.short_ir_sensors.append(self.short3)
        self.short_ir_sensors.append(self.short4)
        self.short_ir_sensors.append(self.short5)
        self.short_ir_sensors.append(self.long0)

        # self.long_ir_sensors = []
        # self.long_ir_sensors.append(self.long0)
        # self.long_ir_sensors.append(self.long1)
        # self.long_ir_sensors.append(self.long2)
        # self.long_ir_sensors.append(self.long3)
        # self.long_ir_sensors.append(self.long4)
        # self.long_ir_sensors.append(self.long5)

        self.ir_count = 0

        self.main_timer = Timer() # setting the timer for wall avoidance
        self.gyro_timer = Timer() # setting the timer for turning
        self.game_timer = None # setting the timer for the servo
        self.turn_timer = None

        # setting up the servos
        self.servo = Servo(self.tamp, PWM7)
        self.servo.write(20)

        #robot movement variables
        self.state = CALCULATING
        self.starting_angle = self.gyro.val
        print "starting angle", self.starting_angle
        self.finding = False
        
        #flapper variables
        self.found_block = False
        self.encoder_initial = 0
        self.detected_color = NOBLOCK
        self.color_count = 0
        self.desired_color_count = 2 #want to read consecutive readings to ascertain color
        self.last_angle = 0

        self.timer = Timer()
        self.cali_timer = Timer()
        self.calibration = 0.0
        self.calibrated = False


    def loop(self):
        # self.test()

        if self.start.val:
            # start the game timer
            if not self.game_timer:
                self.game_timer = Timer()
                self.start_game()

            # After 3 minutes
            if self.game_timer.millis() > 179000:
                self.endgame()


            if self.main_timer.millis() > 100:
                self.main_timer.reset()

                # Color sorting blocks
                self.bitchslap()

                # Check IR Sensors after the first 500 milliseconds.
                if self.game_timer.millis() > 500:
                    self.check_ir_sensors()
            # Transition through states.            
            self.run_state_machine()

    def test(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            # Valid gyro status is [0,1], see datasheet on ST1:ST0 bits
            print "{:6f}, raw: 0x{:08x} = 0b{:032b}".format(self.gyro.val, self.gyro.raw, self.gyro.raw)
        # Janky autocalibration scheme
        if not self.calibrated and self.cali_timer.millis() > 3000:
            drift = self.gyro.val / (self.cali_timer.millis() / 1000.0)
            # Arbitrary calibration tolerance of 0.1 deg/sec
            if abs(drift) > 0.1:
                self.calibration += drift
                print "Calibration:", self.calibration
                self.gyro.calibrate_bias(self.calibration)
            else:
                print "Calibration complete:", self.calibration
                self.calibrated = True
            self.gyro.reset_integration()
            self.cali_timer.reset()

    
    def run_state_machine(self):
        if self.state == CALCULATING:

            # Setting starting angle.
            self.starting_angle = self.gyro.val

            # Get angle and distance from vision thread.
            self.get_angle_and_distance()

            # CALCULATING --> TURNING
            self.state = TURNING

        elif self.state == TURNING:

            # # Initialize timer that tracks how long robot has been turning.
            self.initialize_turn_timer()

            # Every 100 milliseconds, check for desired angle and if we have turned to it.
            # TURNING --> CALCULATING or MOVING
            self.turn_to_desired_angle()                 

        elif self.state == MOVING:
            self.turn_timer.reset()

            self.move_forward()


    def get_angle_and_distance(self):
        global our_color
        global most_recent_angle
        global most_recent_distance 

        # Setting angle and distance received from vision.
        self.angle = most_recent_angle
        self.distance = most_recent_distance

        # Vision does not send us angle or distance info, so still finding.
        if self.angle == None and self.distance == None:
            self.finding = True

    def initialize_turn_timer(self):
        if not self.turn_timer:
            self.turn_timer = Timer()  


    def turn_to_desired_angle(self):

        global our_color
        global most_recent_angle
        global most_recent_distance 

        if self.gyro_timer.millis() > 100:
            self.gyro_timer.reset()

            # Check if robot has turned 360 degrees, and go to farthest sensor if needed.
            self.check_360_turn()

            # Set desired angle.
            if self.farthest_sensor_angle:
                desired_angle = self.farthest_sensor_angle
            else:
                desired_angle = self.angle

            if not desired_angle:
                desired_angle = 360
            print desired_angle

            desired_angle *= DESIRED_SCALING_FACTOR

            # Positive desired angle.
            if desired_angle > 10:
                self.motor1.write(0, TURN_SPEED)
                self.motor2.write(0, TURN_SPEED)

                # Vision is still finding (no angle, no distance) but we just got a reading!
                # TURNING --> CALCULATING
                if self.finding and most_recent_angle:
                    self.state = CALCULATING
                    return

                # Robot has turned to desired angle.
                # TURNING --> MOVING
                if ((self.gyro.val) - self.starting_angle) > desired_angle:
                    self.state = MOVING
                    self.farthest_sensor_angle = None

            # Negative desired angle.      
            elif desired_angle < -10:
                self.motor1.write(1, TURN_SPEED)
                self.motor2.write(1, TURN_SPEED)


                # Vision is still finding (no angle, no distance) but we just got a reading!
                # TURNING --> CALCULATING
                if self.finding and most_recent_angle:
                    self.state = CALCULATING
                    return

                # Robot has turned to desired angle.
                # TURNING --> MOVING 
                if ((self.gyro.val) - self.starting_angle) < desired_angle:
                    self.state = MOVING
                    self.farthest_sensor_angle = None

            # Move forward, no turning needed.
            else:
                self.state = MOVING
                self.farthest_sensor_angle = None

    def check_360_turn(self):
        print (abs(self.gyro.val - self.starting_angle + 360) % 360 )

        if (abs(self.gyro.val - self.starting_angle + 360) % 360 < 10 and self.turn_timer.millis() > TURN_MILLIS):
            self.turn_timer.reset()

            self.set_farthest_sensor_angle()

            self.starting_angle = self.gyro.val

        if self.angle:
            self.turn_timer.reset()


    def set_farthest_sensor_angle(self):

            print "finding farthest sensor..."

            angle = None
            farthest_sensor = 0
            # print short_ir_distance(self.short_ir_sensors[0].val), short_ir_distance(self.short_ir_sensors[1].val), short_ir_distance(self.short_ir_sensors[2].val), short_ir_distance(self.short_ir_sensors[3].val), short_ir_distance(self.short_ir_sensors[4].val), short_ir_distance(self.short_ir_sensors[5].val)
            print "ir", self.ir_readings

            for i in xrange(len(self.ir_readings)):
                if self.ir_readings[i] > farthest_sensor:
                    farthest_sensor = self.ir_readings[i]
                    angle = (i % 6) * 60

            if angle > 180:
                angle -= 360

            # Set the farthest sensor angle to the one we find from the readings.
            self.farthest_sensor_angle = angle
            self.starting_angle = self.gyro.val
            print "farthest_sensor_angle", self.farthest_sensor_angle

    def move_forward(self):
        print "moving forward", self.ir_readings[0], self.ir_readings[6]

        # Move forward until the front IR sensor has something in front of it.
        if ((self.ir_readings[0] > FORWARD_THRESHOLD and self.ir_readings[6] > FORWARD_THRESHOLD) or self.angle):
            self.motor1.write(0,FORWARD_SPEED)
            self.motor2.write(1,FORWARD_SPEED)
        else:
            # MOVING --> CALCULATING
            self.state = CALCULATING
 

    def bitchslap(self): 
        global our_color
        global most_recent_angle
        global most_recent_distance 

        if self.found_block:

            direction = (self.detected_color == our_color)
            sign = 1 - 2 * direction
            done = False

            if (sign*(self.encoder6.val - self.encoder_initial) < 2000):
                # safety check
                if (sign*(self.encoder6.val - self.encoder_initial) < 0):
                    print "something is wrong  -- preventing it from going crazy"
                    done = True
                
                # if stuck for a while, back up a little
                if self.encoder6.val - self.last_angle == 0 and not self.encoder6.val == self.encoder_initial:
                    self.count += 1
                    if self.count > CONSISTENCY_THRESH:
                        self.motor6.write(1 - direction, 20)
                        self.count = 0

                # you gucchi
                else: 
                    self.motor6.write(direction, SLAPPER_SPEED)
                    self.count = 0

            else:
                done = True

            if done:
                self.motor6.write(self.detected_color, 0)
                self.detected_color = NOBLOCK
                self.count = 0
                self.found_block = False

            self.last_angle = self.encoder6.val
        else:
            # print self.color1.r, self.color1.g, self.color1.b
            if (self.color1.r > RED_THRESH * self.color1.g and self.color1.r > RED_THRESH * self.color1.b) \
            or (self.color2.r > RED_THRESH * self.color2.g and self.color2.r > RED_THRESH * self.color2.b):
                if self.detected_color == RED:
                    self.count = self.count + 1
                else:
                    self.detected_color = RED
                    self.count = 0
            elif (self.color1.g > GREEN_THRESH * self.color1.r and self.color1.g > GREEN_THRESH * self.color1.b) \
            or (self.color2.g > GREEN_THRESH * self.color2.r and self.color2.g > GREEN_THRESH * self.color2.b):
                if self.detected_color == GREEN:
                    self.count = self.count + 1
                else:
                    self.detected_color = GREEN
                    self.count = 0

            if not self.detected_color == NOBLOCK and self.count >= CONSISTENCY_THRESH:
                print "color is", self.detected_color
                self.encoder_initial = self.encoder6.val
                self.found_block = True
                self.speed = 0
                self.count = 0

    def check_ir_sensors(self):
        # Get the sensor readings and find the distances

        for i in xrange(len(self.ir_readings)):
            ir_reading = self.short_ir_sensors[i].val / 1000.0
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
        if (too_close_count_1 >= len(STUCK_SENSORS_1) or too_close_count_2 >= len(STUCK_SENSORS_2)) and self.angle == None:
            # Make sure we get a stuck reading 3 times before we declare it stuck.
            self.ir_count += 1

            if self.ir_count >= 3:
                # Stuck, and turning now. Reset the reading count.
                print "stuckkk :("
                self.state = TURNING
                self.ir_count = 0
        else:
            self.ir_count = 0

    def start_game(self):

        global our_color
        global most_recent_angle
        global most_recent_distance 

        self.motor3.write(0, 75)
        self.motor5.write(0, 100)
        # figure out our color
        our_color = self.color_led.val

        print "color", self.color_led.val

        #close our door
        self.servo.write(20)

        #vision
        camera = setup_vision()
        thread_vision = Thread( target=vision_thread, args=(camera,))
        thread_vision.daemon = True
        thread_vision.start()

    def endgame(self):
        global our_color
        global most_recent_angle
        global most_recent_distance 

        print "Game Over!"
        our_color = self.color_led.val #double check
        self.servos[0].write(our_color * 180)



if __name__ == "__main__":


    sketch = Movement(15,-0.00001, 100)
    sketch.run()
   
    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, set_end)
    
    time.sleep(10000)
