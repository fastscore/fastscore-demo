# fastscore.recordsets.0: true
# fastscore.recordsets.1: true
# fastscore.module-attached: gensim
# fastscore.module-attached: xgboost

import pickle
import gensim
import pandas as pd
import numpy
import sys
import xgboost

def pad_vectors(list_of_vecs):
    for j in range(len(list_of_vecs), 2**2):
        list_of_vecs.append(numpy.zeros(2**2))
    return numpy.array(list_of_vecs)

def preprocess(df):
    tokens = df.content.astype(str).apply(lambda x: list(gensim.utils.tokenize(x)))
    tokens = tokens.apply(lambda x: x[:2**2])
    vectorized = tokens.apply(lambda x: list(map(lambda y: ft_model.wv[y], x)))
    padded_vectors = vectorized.apply(pad_vectors)
    padded_vectors = padded_vectors.apply(lambda x: x.flatten())
    data = padded_vectors.to_list()
    data = numpy.array(data)
    data = pd.DataFrame(data, index = padded_vectors.index, columns = range(2**4))
    return data

# modelop.init
def begin():
    global threshold, xgb_model, ft_model
    xgb_model_artifacts = pickle.load(open('/fastscore/xgb_model_artifacts.pkl', 'rb'))
    threshold = xgb_model_artifacts['threshold']
    ft_model = xgb_model_artifacts['ft_model']

    xgb_model = xgboost.XGBClassifier()
    xgb_model.load_model('/fastscore/xgb_model.model')
    pass

# modelop.score
def action(df):
   
    cleaned = preprocess(df)
    pred_proba = xgb_model.predict_proba(cleaned)[:,1]
    pred_proba = pd.Series(pred_proba, index = df.index)
    preds = pred_proba.apply(lambda x: x > threshold).astype(int)


    output = pd.concat([df, preds], axis=1)
    output.columns = ['id', 'content', 'prediction']
    yield output

