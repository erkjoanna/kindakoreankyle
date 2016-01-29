from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Color

# Prints RGB, clear(C), colorTemp, and lux values read and
# computed from the device. For more details, see the Adafruit_TCS34725
# Arduino library, from which the colorTemp and lux computations are
# used.

# Color sensor should be connected to the I2C ports (SDA and SCL)

class ColorRead(SyncedSketch):

    def setup(self):
        self.color = Color(self.tamp, 0,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.color1 = Color(self.tamp, 1,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.timer = Timer()
	self.count = 0

    def loop(self):
        if self.timer.millis() > 100:
		self.count += 1
		if self.count % 10 == 0:
			print "--"
		self.timer.reset()
		red = 1.3
		if (self.color.r > red * self.color.g and self.color.r > red * self.color.b):
			print "1 is red"
		if (self.color1.r > red * self.color1.g and self.color1.r > red * self.color1.b):
			print "2 is red"
		green = 1.2
		if (self.color.g > red * self.color.r and self.color.g > red * self.color.b):
			print "1 is green"
		if (self.color1.g > red * self.color1.r and self.color1.g > red * self.color1.b):
			print "2 is green"


if __name__ == "__main__":
    sketch = ColorRead(1, -0.00001, 100)
    sketch.run()
