# fastscore.schema.0: double
# fastscore.schema.2: double
# fastscore.slot.1: unused
# fastscore.module-attached: streamstats
# fastscore.module-attached: influxdb


from streamstats import *
import sys
import datetime as dt
from influxdb import InfluxDBClient
from time import sleep

def vals_to_dict(sb):
	vals = sb.values
	mean, var = vals["Moments"]
	vals["Mean"] = mean
	vals["Variance"] = var
	del vals["Moments"]
	ewma, ewmv = vals["EWM"]
	vals["EWMA"] = ewma
	vals["EWMV"] = ewmv
	del vals["EWM"]
	return {**vals}

def gen_point(name,datum,timestamp,prefix):
    point = {
        "measurement": name,
        "time": timestamp,
        "fields": {
            "{}_Max".format(prefix): datum['Max'],
            "{}_Min".format(prefix): datum['Min'],
            "{}_Mean".format(prefix): datum['Mean'],
            "{}_Variance".format(prefix): datum['Variance'],
            "{}_EWMA".format(prefix): datum['EWMA'],
            #"EWMV": datum['EWMV'],
            "{}_prediction".format(prefix): datum['prediction'],
            "{}_Elapsed Time".format(prefix): datum['Elapsed Time'],
            "{}_Number of Records".format(prefix): datum['Number of Records']
        }
    }
    return point


def begin():

    # define your cases

	global influx, FLUSH_DELTA, BATCH_SIZE, BATCH
	global bundle1, bundle2, bundlediff
	global num_of_recs
	global buffer
	num_of_recs = 0

	bundle1 = StreamingCalcBundle()
	bundle2 = StreamingCalcBundle()
	bundlediff = StreamingCalcBundle()

    # Add the streaming calculations we want to track

	for bundle in [bundle1, bundle2, bundlediff]:
		bundle + StreamingCalc(update_moments, name='Moments', val=(0.0, 0.0))
		bundle + StreamingCalc(update_ewm, name='EWM', val = (0.0,0.0))
		bundle + StreamingCalc(update_max, name='Max')
		bundle + StreamingCalc(update_min, name='Min')

	FLUSH_DELTA = 1.0
	BATCH_SIZE = 1
	BATCH = []
	influx = InfluxDBClient('influxdb', '8086', 'admin', 'scorefast', 'fastscore')

	# buffer inputs
	buffer = {0: [], 2: []}


def action(predict, slot):
	global buffer

	buffer[slot].append(predict)

	while all([len(buffer[i]) > 0 for i in buffer]):
		top = { i: buffer[i][0] for i in buffer }
		buffer = { i : buffer[i][1:] for i in buffer }
		do_update(top)


def do_update(top):
	global bundle1, bundle2, bundlediff
	global start_time
	global num_of_recs
	global BATCH

	x1 = top[0]
	x2 = top[2]

	name = "monitors"

	timestamp = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
	num_of_recs += 1
	if num_of_recs == 1:
		start_time = dt.datetime.now().timestamp()
	current_time = dt.datetime.now().timestamp()
	elapsed_time = current_time - start_time

	bundle1.update(x1)
	bundle2.update(x2)
	bundlediff.update(x1 - x2)


	report1 = vals_to_dict(bundle1)
	report1['Elapsed Time'] = float(elapsed_time)
	report1["Number of Records"] = float(num_of_recs)
	report1["prediction"] = x1

	report2 = vals_to_dict(bundle2)
	report2['Elapsed Time'] = float(elapsed_time)
	report2['Numer of Records'] = float(num_of_recs)
	report2['prediction'] = x2

	reportdiff = vals_to_dict(bundlediff)
	reportdiff['Elapsed Time'] = float(elapsed_time)
	reportdiff['Number of Records'] = float(num_of_recs)
	reportdiff['prediction'] = x1 - x2

	point = gen_point(name, report1, timestamp, prefix="Model1")
	point.update(gen_point(name, report2, timestamp, prefix="Model2"))
	point.update(gen_point(name, reportdiff, timestamp, prefix="Diff"))

	BATCH.append(point)
	if BATCH_SIZE == len(BATCH):
		influx.write_points(BATCH)
		sys.stdout.flush()
		BATCH = []
		sleep(FLUSH_DELTA)
