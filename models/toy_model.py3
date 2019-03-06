# fastscore.schema.0: input_schema
# fastscore.schema.1: output_schema


import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
import sys
import pandas as pd


def begin():
    global fit
    fit = pickle.load(open('test.pkl', 'rb'))

def action(x):
    ev_id = x['EV_ID']
    pred = fit.predict(pd.Series(x).values.reshape(1,-1))[0]
    yield dict(EV_ID=ev_id, MULTI_CTGY_PRED=pred)