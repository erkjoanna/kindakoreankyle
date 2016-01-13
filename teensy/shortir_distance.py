from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import AnalogInput
from voltage_distance_converter import *

# Detects changes in allllll the pins!

class AnalogRead(SyncedSketch):

    adc_pin = 11

    def setup(self):
        self.testpin = AnalogInput(self.tamp, self.adc_pin)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print self.testpin.val, self.testpin.val/1000.0, long_ir_distance(self.testpin.val/1000.0)

if __name__ == "__main__":
    sketch = AnalogRead(1, -0.00001, 100)
    sketch.run()