from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro, Motor
from constants import *
from threading import Thread
from vision import *

color = RED
most_recent_angle = 0
most_recent_distance = 0

def thread1():
    global color
    global most_recent_angle
    global most_recent_distance
    while True:
       most_recent_angle, most_recent_distance = vision(color)

class Movement (SyncedSketch):

    global color
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
        self.timer = Timer() #setting the timer

        self.state = CALCULATING
        self.starting_angle = self.gyro.val
        self.desired_angle = 0
        

    def loop(self):
        if self.state == CALCULATING:
            angle = most_recent_angle
            distance = most_recent_distance
            self.starting_angle = self.gyro.val
            self.state = TURNING
        elif self.state == TURNING:
            #take a snapshot of the current gyro number

            #while the robot hasn't turned desired degrees yet
            if self.timer.millis()>100:
                print "starting_angle: ", self.starting_angle #check
                print "difference: ",(self.gyro.val)-self.starting_angle
                self.timer.reset()
                if self.desired_angle > 0:
                    self.motor1.write(0,10)
                    self.motor2.write(0,10)
                    if ((self.gyro.val) - self.starting_angle) > self.desired_angle:
                        self.state = MOVING        
                elif self.desired_angle < 0:
                    self.motor1.write(1,10)
                    self.motor2.write(1,10)
                    if ((self.gyro.val) - self.starting_angle) < self.desired_angle:
                        self.state = MOVING
                else:
                    self.state = MOVING
        elif self.state == MOVING:
            #move the robot forward for a second - THIS DOESN'T QUITE WORK YET
            if self.timer.millis() > 8000:
                self.motor1.write(1,10)
                self.motor2.write(0,10)             
                self.state = CALCULATING
                self.timer.reset()

if __name__ == "__main__":
    thread_vision = Thread( target=thread1, args=())
    thread_vision.start()

    sketch = Movement(3,-0.00001, 100)
    sketch.run()
