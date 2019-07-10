# fastscore.schema.0: close_price_truth
# fastscore.schema.1: tagged_mse

import numpy as np
import pickle
import time
from sklearn.linear_model import LinearRegression


def begin():
    global lr
    global window, window_size
    window = []
    window_size = 15
    with open('lr_pickle1.pkl', 'rb') as f:
        lr = pickle.load(f)

def action(x):
    time.sleep(3)
    global window, window_size
    actual = x['Actual']
    x = x['Close']
    window = window[1-window_size:] + [x]
    if len(window) < window_size:
        yield {"name": "price", "value":x, "mse": (x-actual)**2}
    else:
        X = np.array([window])
        y = lr.predict(X)
        yield {"name":"price", "value": y[0,0], "mse": (y[0,0]-actual)**2}