# fastscore.schema.0: input_schema
# fastscore.schema.1: output_schema


import numpy as np
import pickle
from sklearn.linear_model import LinearRegression


def begin():
    global WORD_LIST 
    WORD_LIST = ['WORD_1',
                'WORD_2',
                'WORD_3',
                'WORD_4',
                'WORD_5',
                'WORD_6',
                'WORD_7',
                'WORD_8',
                'WORD_9']

def action(x):
    sum_of_words = sum([x[w] for w in WORD_LIST])
    if sum_of_words % 2 == 0:
        score = dict(EV_ID = str(x['EV_ID']), MULTI_CTGY_PRED = sum_of_words, TRAN_CTGY_CD_PRED = 'FOO')
    else:
        score = dict(EV_ID = str(x['EV_ID']), MULTI_CTGY_PRED = sum_of_words, TRAN_CTGY_CD_PRED = 'BAR')
    print(score)

    yield score