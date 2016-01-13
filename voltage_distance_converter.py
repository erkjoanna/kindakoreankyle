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
		print "Distance is less than 3cm."
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
	# short_equation = 
	# inv_voltage = 0.07833*distance + 0.01075
	inv_voltage = 1/v
	distance = (inv_voltage - 0.01075) / 0.07833

	# Distances less than 3cm are wack on Short IR
	if distance < 3:
		return -1
	else:
		return distance

'''
Returns distance given Long IR Sensor's voltage reading
'''
def long_ir_distance(v):
	inv_voltage = 1/v

	# y = 0.01359225304*x + 0.1238025628
	# inv_voltage = 0.01359225304*distance + 0.1238025628
	distance = (inv_voltage - 0.1238025628) / 0.01359225304

	# Distances less than 15cm are wack on Long IR
	if distance < 15:
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
