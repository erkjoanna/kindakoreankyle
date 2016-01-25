from vision import *
from constants import *

start = time.time()
camera = setup_vision()
for i in range(10):
	vision(camera, GREEN)
cleanup_vision(camera)
print "totaltime", time.time() - start
