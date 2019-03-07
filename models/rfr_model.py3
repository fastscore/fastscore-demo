# fastscore.schema.0: example_input
# fastscore.schema.1: tagged_double


import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder



def begin():
    #It's necessary to set these variables as global so they will be scoped to use in the "action" function.
    global enc
    global rfr
    enc = pickle.load(open('onehotenc.pkl', 'rb'))
    rfr = pickle.load(open('example_model.pkl', 'rb'))

def action(x):
    #In this example, FastScore will parse x as a Python dictionary since x is a single record.
    #print(x)
    ID = x['id']
    word = x['word']
    one_hot = enc.transform(np.array(word).reshape(-1,1)).toarray()[0].reshape(1,-1)
    feats = np.array([x['feat_1'], x['feat_2']]).reshape(1,-1)
    #print(one_hot.shape)
    #print(feats.shape)
    sample = np.concatenate([feats,one_hot], axis=1)
    pred = rfr.predict(sample)[0]
    yield dict(id=ID, pred=pred)