import sys
from signal import *
from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro, Motor, Color
from constants import *
from threading import Thread
from vision import *

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

        #setting motor orientations (for fun)
        self.motor1.write(1,0) #1 is forward for Motor 1
        self.motor2.write(0,0) #0 is forward for Motor 2
        
        #setting the timer
        self.timer = Timer() #setting the timer
        self.timer2 = Timer() #setting the timer

        #setting up the color sensor
        self.color = Color(self.tamp, integrationTime=Color.INTEGRATION_TIME_101MS, gain=Color.GAIN_1X)

        #robot movement variables
        self.state = CALCULATING
        self.starting_angle = self.gyro.val     
        
        #flapper variables
        self.detected_color = NOBLOCK
        self.color_count = 0
        self.desired_color_count = 2 #want to read consecutive readings to ascertain color

    def loop(self):
        if self.timer2.millis()>100:
            self.timer2.reset()
            self.color_sorting()

        if self.state == CALCULATING:
            angle = most_recent_angle
            distance = most_recent_distance

            # Vision does not see any color, rotate in place.
            if angle == None and distance == None:
                self.angle = 360

            self.starting_angle = self.gyro.val
            self.state = TURNING

        elif self.state == TURNING:
            #take a snapshot of the current gyro number

            #while the robot hasn't turned desired degrees yet
            if self.timer.millis()>100:
                #print "starting_angle: ", self.starting_angle #check.
                print "difference: ",(self.gyro.val)-self.starting_angle
                self.timer.reset()
                if most_recent_angle > 0:
                    self.motor1.write(0,10)
                    self.motor2.write(0,10)
                    if ((self.gyro.val) - self.starting_angle) > most_recent_angle:
                        self.state = MOVING        
                elif most_recent_angle < 0:
                    self.motor1.write(1,10)
                    self.motor2.write(1,10)
                    if ((self.gyro.val) - self.starting_angle) < most_recent_angle:
                        self.state = MOVING
                else:
                    self.state = MOVING
        elif self.state == MOVING:
            #move the robot forward for a second - THIS DOESN'T QUITE WORK YET
            self.motor1.write(1,10)
            self.motor2.write(0,10) 
            
            if self.timer.millis() > 3000:            
                self.state = CALCULATING
                self.timer.reset()

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
