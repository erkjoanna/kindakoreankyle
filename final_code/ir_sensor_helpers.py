'''
Params:
short_ir_v - Short IR voltage reading
long_ir_v - Long IR voltage reading

Returns tuple pairs of actual distance given voltage
readings from both the Short IR and Long IR sensors
'''
def voltage_to_distance(short_ir_v, long_ir_v):

	short_d = short_ir_distance(short_ir_v)
	long_d = long_ir_distance(long_ir_v)

	if (short_d == -1):
		# Distance is less than 3cm
		return (None, None)
	elif (long_d == -1):
		# Distance is between 3cm and 10cm
		return (short_d, None)
	else:
		# Distance is longer than 10cm
		return (short_d, long_d)

'''
Returns distance given Short IR Sensor's voltage reading
'''
def short_ir_distance(v):
	if v == 0:
		return -1

	inv_voltage = 1/v
	distance = (inv_voltage - 0.008073087974) / 0.00565114114

	# Inverse Voltages less than 0.0088 are not accurate
	if inv_voltage < 0.0088:
		return -1
	else:
		return distance

'''
Returns distance given Long IR Sensor's voltage reading
'''
def long_ir_distance(v):

	if v == 0:
		return -1

	inv_voltage = 1 / v

	# y = 0.0012214883*x -0.003449589563
	# inv_voltage = 0.0012214883 * distance - 0.003449589563
	distance = (inv_voltage + 0.003449589563) / 0.0012214883

	# inv_voltage = -0.6872953134 * distance + 9.326933936
	# Distances less than 15cm are wack on Long IR
	if inv_voltage < 0.024:
		return -1
	else:
		return distance



def drange(start, stop, step):
    r = start
    while r < stop:
    	yield r
    	r += step

def demo():
	for i in drange(0.1, 3.5, 0.1):
		print "V = ", i, voltage_to_distance(i, i)
