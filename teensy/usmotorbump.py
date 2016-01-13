from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import DigitalOutput, DigitalInput, Motor 

#WORKS :D :D :D 
#Robot should continuously move forward
#If the robot detects something 4-10cm in front, it will back off
#USS pin
USS = 32

#Motor Pins
DIR1 = 27
PWM1 = 3
DIR2 = 28
PWM2 = 23

class MotorUS(SyncedSketch):
    
    def setup(self):
        self.usread = DigitalInput(self.tamp, USS) #read USS pin
        self.motor1 = Motor(self.tamp, DIR1, PWM1) #read motor1
        self.motor2 = Motor(self.tamp, DIR2, PWM2) #read motor2
        self.motor1.write(1,0) #self.motor1.write(direction, speed)
        self.motor2.write(1,0) #1 = forward, 0 = backward for direction
    def loop(self):

        if self.usread.changed:
            print self.usread.val
        
        #if there is NOTHING in front of the robot
        if self.usread.val == 1:
            self.motor1.write(1, 100) #motor 1 positive is forward
            self.motor2.write(0, 100) #motor 2 negative is forward

        #if there is SOMETHING in front of the robot
        else:
            self.motor1.write(0,100)
            self.motor2.write(1,100)
            
if __name__ == "__main__":
    sketch = MotorUS(3, -0.00001, 100)
    sketch.run()
