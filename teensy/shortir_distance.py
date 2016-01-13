from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import AnalogInput
from voltage_distance_converter import *
import numpy as np

class AnalogRead(SyncedSketch):

    adc_pin = 13

    def setup(self):
        self.testpin = AnalogInput(self.tamp, self.adc_pin)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print self.testpin.val/1000.0, "short ir reading: ", short_ir_distance(self.testpin.val/1000.0)

if __name__ == "__main__":
    sketch = AnalogRead(1, -0.00001, 100)
    sketch.run()