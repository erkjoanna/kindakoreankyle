#motor pins dir1: pin27 dir2: pin28 pwm1: pin3 pwm2: pin23
#shortir sensor is on pinA13. define the pin as only "13" and teensy recognizes
    #the input as an analog signal
#use the short_ir_disance function in voltage_distance_converter.py file
#import voltage_distance_converter.py in the header lines of the file
#make sure to divide the analog read value by 1000 before passing it to the short_ir_distance
    #function. 
#use shortir_distance.py as a reference and example file for reading the shortir sensor value
from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

class MotorWrite(Sketch):

    def setup(self):
        self.motor = Motor(self.tamp, 2, 3)
        self.motor.write(1,0)
        self.delta = 1
        self.motorval = 0
        self.timer = Timer()

    def loop(self):
        if (self.timer.millis() > 10):
            self.timer.reset()
            if abs(self.motorval) == 255: self.delta = -self.delta
            self.motorval += self.delta
            self.motor.write(self.motorval>0, abs(self.motorval))

if __name__ == "__main__":
    sketch = MotorWrite()
    sketch.run()


class avoid_obsacles(Sketch):

    def setup(self):
        self.motor = Motor(self.tamp, 3, 23)

