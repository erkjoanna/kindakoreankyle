from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Gyro, Motor

#Reads gyro and turns directions accordingly

class GyroMotor (SyncedSketch):

    #set pins
    #if pin descriptions are inside class, must be inserted as
    #self.pin in the arguments
    GYRO = 10
    DIR1 = 27
    DIR2 = 28
    PWM1 = 3
    PWM2 = 23

    def setup(self):
        self.gyro = Gyro(self.tamp, self.GYRO, integrate = True)
        self.motor1 = Motor(self.tamp, self.DIR1, self.PWM1)
        self.motor2 = Motor(self.tamp, self.DIR2, self.PWM2)
        self.motor1.write(1,0) #1 is forward for Motor 1
        self.motor2.write(0,0) #0 is forward for Motor 2
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            # Valid gyro status is [0,1], see datasheet on ST1:ST0 bits
            print self.gyro.val, self.gyro.status
        if (self.gyro.val < 20):
            self.motor1.write(0,10)
            self.motor2.write(0,10)
        elif (self.gyro.val > 50):
            self.motor1.write(1,10)
            self.motor2.write(1,10)
        else:
            self.motor1.write(1,50)
            self.motor2.write(0,50)
            
        
if __name__ == "__main__":
    sketch = GyroMotor(3,-0.00001, 100)
    sketch.run()
