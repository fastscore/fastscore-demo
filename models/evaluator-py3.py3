# fastscore.schema.0: lr-mont
# fastscore.schema.1: report
# fastscore.module-attached: streamstats


from streamstats import *
import sys
import datetime as dt


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
    

def begin():
    
    # define your cases
    
	global bundle
	global num_of_recs
	num_of_recs = 0
    
	bundle = StreamingCalcBundle()
    
    # Add the streaming calculations we want to track
	
	bundle + StreamingCalc(update_moments, name='Moments', val=(0.0, 0.0))
	bundle + StreamingCalc(update_ewm, name='EWM', val = (0.0,0.0))
	bundle + StreamingCalc(update_max, name='Max')
	bundle + StreamingCalc(update_min, name='Min')

def action(predict):
	global bundle
	global start_time
	global num_of_recs
	num_of_recs += 1
	if num_of_recs == 1:
		start_time = dt.datetime.now().timestamp()
	current_time = dt.datetime.now().timestamp()
	elapsed_time = current_time - start_time
	prediction = predict["score"]	
	bundle.update(x=prediction)    
    
	
	report = vals_to_dict(bundle)
        report['score'] = prediction
	
	report['Elapsed Time'] = float(elapsed_time)
	report["Number of Records"] = float(num_of_recs)
	print(report)
	sys.stdout.flush()
	
	yield report
