from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor, Encoder
import numpy as np

class SignalInputOutput(SyncedSketch):
		'set the encoder pins'
		encoderpins = 30,33
	def setup(self):
		self.encoder = Encoder(self.tamp, *self.encoderpins, continuous=True)
		self.motor = Motor(self.tamp, 27, 3)
		self.timer = Timer()
		self.toward = 1

	def loop(self):
		'send motor a distance, feedback estimate travel'
		distance = 30 #distance in centimeters
		if self.timer.millis() > 100:
			print self.encoder.val
			self.timer.reset()
		'if encoder value is grater than the distance, change toward to 0'
		if self.encoder.val > 30:
			self.toward = 0
		'if toward == 1, keep moving towards'
		if self.toward:
			self.motor.write(1,30) #direction and speed