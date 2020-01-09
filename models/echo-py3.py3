# fastscore.slot.0: in-use
import sys as sys


# modelop.score
def action(datum):
	sys.stdout.flush()
	print(datum)
	sys.stdout.flush()

	yield datum


def metrics(datum):
	yield "{ \"foo\": 1 }"


# modelop.metrics
def dict_metrics(datum):
	sys.stdout.flush()
	print("metrics function called: " + datum)
	sys.stdout.flush()

	yield {
		"foo": 1,
		"bar": "test result"
	}
