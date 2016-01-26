from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

DIR1 = 25
PWM1 = 4
PWM2 = 5

class MotorWrite(Sketch):

    def setup(self):
        self.motor = Motor(self.tamp, DIR1, PWM1)
        self.motor2 = Motor(self.tamp, DIR1, PWM1)
        self.motor3 = Motor(self.tamp, DIR1, PWM2)
        self.motor.write(1,0)
        self.delta = 1
        self.motorval = 0
        self.timer = Timer()

    def loop(self):
        if (self.timer.millis() > 10):
            self.timer.reset()
            self.motor.write(1, 50)
            self.motor2.write(1, 50)
            self.motor3.write(1, 60)

if __name__ == "__main__":
    sketch = MotorWrite()
    sketch.run()