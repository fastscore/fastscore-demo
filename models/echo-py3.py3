import sys as sys


# modelop.score
def action(datum):
	sys.stdout.flush()
	print(datum)
	
	yield(datum)


# modelop.metrics
def metrics(datum):
	yield("{ foo: 1 }");
