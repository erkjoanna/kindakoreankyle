from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import AnalogInput, Motor 
from voltage_distance_converter import *
import numpy as np

class MotorShortIR(SyncedSketch):

    adc_pin = 13

    #Motor Pins
    DIR1 = 27
    PWM1 = 3
    DIR2 = 28
    PWM2 = 4

    def setup(self):
        self.short_ir = AnalogInput(self.tamp, self.adc_pin)
        self.motor1 = Motor(self.tamp, self.DIR1, self.PWM1) #read motor1
        self.motor2 = Motor(self.tamp, self.DIR2, self.PWM2) #read motor2
        self.motor1.write(1,0) #self.motor1.write(direction, speed)
        self.motor2.write(1,0) #1 = forward, 0 = backward for direction
        self.timer = Timer()

    def loop(self):

        short_ir_reading = short_ir_distance(self.short_ir.val / 1000.0)
        
        # if there is something greater 5 centimeters from the IR sensor
        if short_ir_reading > 8.0:
            self.motor1.write(1, 10) #motor 1 positive is forward
            self.motor2.write(0, 10) #motor 2 negative is forward

        # else (there is something within 5 centimeters from the IR sensor)
        else:
            self.motor1.write(0,10)
            self.motor2.write(1,10)


        # if self.timer.millis() > 100:
        #     self.timer.reset()
        #     print self.testpin.val/1000.0, "short ir reading: ", short_ir_distance(self.testpin.val/1000.0)

if __name__ == "__main__":
    sketch = MotorShortIR(3, -0.00001, 100)
    sketch.run()