import sys as sys
import time

def action(datum):
	# I'm sleeping here so this model will error out with a default roundtrip REST transport
	time.sleep(20)
	sys.stdout.flush()
	print(datum)
	
	yield(datum)
