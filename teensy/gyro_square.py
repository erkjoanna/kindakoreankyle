from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro, Motor

#let's move in a square! :D :D :D 

class GyroSquare (SyncedSketch):

    #set pins
    #if pin descriptions are inside class, must be inserted as
    #self.pin in the arguments
    GYRO = 10
    DIR1 = 27
    DIR2 = 28
    PWM1 = 3
    PWM2 = 4

    def setup(self):
        #setting up the gyro and two motors
        self.gyro = Gyro(self.tamp, self.GYRO, integrate = True)
        self.motor1 = Motor(self.tamp, self.DIR1, self.PWM1)
        self.motor2 = Motor(self.tamp, self.DIR2, self.PWM2)

        #setting motor orientations (for fun)
        self.motor1.write(1,0) #1 is forward for Motor 1
        self.motor2.write(0,0) #0 is forward for Motor 2
        self.timer = Timer() #setting the timer

    def loop(self):
        '''
        #see how the gyro is doing
        if self.timer.millis() > 100:
            self.timer.reset()
            # Valid gyro status is [0,1]
            print self.gyro.val, self.gyro.status

        '''
        #take a snapshot of the current gyro number
        peek = self.gyro.val
        print "peek: ",peek #check

        ninetydegrees =  30

        #while the robot hasn't turned 90 degrees yet
        while ((self.gyro.val)-peek) < ninetydegrees:
	    if self.timer.millis()>100:
                self.timer.reset()
	    	print peek, "difference: ",(self.gyro.val)-peek, "raw: ",self.gyro.val
 #check to see if this works lol, value should increase
        
	#move the robot forward for a second - THIS DOESN'T QUITE WORK YET
        while self.timer.millis()<2000:
	    x = 1 
        self.motor1.write(1,50)
        self.motor2.write(0,50)     	    
        self.timer.reset()
        print "In if loop."  

if __name__ == "__main__":
    sketch = GyroSquare(3,-0.00001, 100)
    sketch.run()
