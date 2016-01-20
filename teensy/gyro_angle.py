from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro, Motor

#let's move in a square! :D :D :D 

class GyroSquare (SyncedSketch):

    #set pins
    #if pin descriptions are inside class, must be inserted as
    #self.pin in the arguments
    GYRO = 10
    DIR1 = 28
    DIR2 = 27
    PWM1 = 4
    PWM2 = 3

    #states
    TURNING = 0
    MOVING = 1 
    GOAL_ANGLE = 20

    def setup(self):
        #setting up the gyro and two motors
        self.gyro = Gyro(self.tamp, self.GYRO, integrate = True)
        self.motor1 = Motor(self.tamp, self.DIR1, self.PWM1)
        self.motor2 = Motor(self.tamp, self.DIR2, self.PWM2)

        #setting motor orientations (for fun)
        self.motor1.write(1,0) #1 is forward for Motor 1
        self.motor2.write(0,0) #0 is forward for Motor 2
        self.timer = Timer() #setting the timer

        self.state = self.TURNING 

    def loop(self):
        if self.state == self.TURNING:
            #take a snapshot of the current gyro number
            peek = self.gyro.val 
            print "peek: ", peek

            #move the robot until it reaches the goal angle change
            while ((self.gyro.val)-peek) < self.GOAL_ANGLE:
                #checking the change in angle
                if self.timer.millis()>100:
                    self.timer.reset()
                    print "difference: ", (self.gyro.val)-peek, peek 
                    #change the angle
                    self.motor1.write(0,25)
                    self.motor2.write(0,25)
            
            #now change the robot setting
            self.state = self.MOVING

        elif self.state == self.MOVING:
            #move the robot forward for two seconds
            if self.timer.millis()>8000:
                self.timer.reset()
                print "Going straight! :)"
                self.motor1.write(1,50)
                self.motor2.write(0,50)
                self.state = self.TURNING

if __name__ == "__main__":
    sketch = GyroSquare(3,-0.00001, 100)
    sketch.run()
