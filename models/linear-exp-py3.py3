# fastscore.action: unused

# fastscore.schema.0: close_price
# fastscore.schema.1: tagged_double


import numpy as np
import pickle
from sklearn.linear_model import LinearRegression


from fastscore.io import Slot


window = []
window_size = 15

with open('lr_pickle1.pkl', 'rb') as f:
    lr = pickle.load(f)


for df in Slot(0):
    x = df['Close']
    window = window[1-window_size:] + [x]
    if len(window) < window_size:
            Slot(1).write({"name": "price", "value":x})

    else:
        X = np.array([window])
        y = lr.predict(X)
        Slot(1).write({"name": "price", "value": y[0,0]})
