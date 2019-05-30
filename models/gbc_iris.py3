#fastscore.schema.0: iris_input.avsc
#fastscore.schema.1: string.avsc
#fastscore.recordsets.0: true
#fastscore.recordsets.1: true

from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import pickle

def begin():
    global model
    with open('gbc.pkl', 'rb') as f:
        model = pickle.load(f)
    pass

def action(x):
    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    df = x[features] 
    preds = pd.Series(model.predict(df.loc[:,features]))
    translate = {0:'Setosa', 1:'Versicolour', 2:'Virginica'}
    output = preds.apply(lambda x: translate[x])
    yield output 
