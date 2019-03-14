# fastscore.input: lr-mont 

# fastscore.module-attached: influxdb


from influxdb import InfluxDBClient
from datetime import datetime
from time import sleep

# mean and std dev of MSE - the last n - half a std deviation mean should be close to 0, 
# 10 


def begin():
    global influx, FLUSH_DELTA, BATCH_SIZE, BATCH, N, MSE, value_list
    
    FLUSH_DELTA = 0.01
    BATCH_SIZE = 10
    BATCH = []
    N = 0
    
    influx = InfluxDBClient('influxdb', '8086', 'admin', 'scorefast', 'fastscore')

def gen_point(name, actual, prediction, MSE, timestamp):
    point = {
        "measurement": name,
        "time": timestamp,
        "fields": {
            "predicted": value,
            "actual": actual,
            "MSE": MSE,
            "timestamp": timestamp
        }
    }
    return point

def MSE(actual,predicted):

    MSE = (1/N)*(N*MSE+(predicted - actual) ** 2)
    N = N + 1
    return MSE

def action(datum):
    global BATCH
    
    name = datum['name']
    actual = datum['monitor']
    predicted = datum['value']

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    MSE = MSE(actual, predicted)
    BATCH.append(gen_point(name, actual, prediction, MSE, timestamp))

    if BATCH_SIZE == len(BATCH):
        #influx.write_points(BATCH)
        print(BATCH)
        BATCH = []
        sleep(FLUSH_DELTA)
