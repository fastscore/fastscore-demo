# fastscore.schema.0: double
# fastscore.schema.1: double

import numpy as np

def begin():
    global window, window_size, coeffs
    window = []
    window_size = 15
    coeffs = np.random.rand(15) # random coefficients

def action(x):
    global window, window_size, coeffs

    window = window[1 - window_size:] + [x]
    if len(window) < window_size:
        yield x
    else:
        yield (coeffs + np.random.rand(15)/5).dot(window).item()
