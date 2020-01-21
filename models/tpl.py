# fastscore.module-attached: tensorflow

import pandas as pd
import json
import re
from tensorflow.contrib import learn
import os
import numpy as np
import tensorflow as tf

# CNN Model
def begin():
    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore("/fastscore/vocab") #reads trained model

    global graph, sess, input_x, dropout_keep_prob, predictions
    model_name = 'tpl'

    graph = tf.Graph()
    session_conf = tf.ConfigProto(
        allow_soft_placement=True,
        log_device_placement=False)
    sess = tf.Session(config=session_conf)

    # Load the saved meta graph and restore variables
    saver = tf.train.import_meta_graph("{}.meta".format(model_name)) # meta graph and variables are saved under
    # attachment.tar.gz
    saver.restore(sess, './{}'.format(model_name))

    # Get the placeholders from the graph by name
    input_x = sess.graph.get_operation_by_name("input_x").outputs[0]
    dropout_keep_prob = sess.graph.get_operation_by_name("dropout_keep_prob").outputs[0]
    # Tensors we want to evaluate
    predictions = sess.graph.get_operation_by_name("output/predictions").outputs[0]

def action(x):
    df = pd.DataFrame([x])
    n_clm = df['ClaimNumber']
    ld = df['LossDescription'].astype(str)
    x_raw = [clean_str(x) for x in ld]
    x_test = np.array(list(vocab_processor.transform(x_raw)))

    score = sess.run(predictions, {input_x: x_test, dropout_keep_prob: 1.0})

    output = {'ClaimNumber': n_clm[0], 'Score': score[0]}

    yield output

def end():
    sess.close()

def clean_str(string):
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)

    ret = string.strip().lower()
    if not ret:
        ret = ''.join(random.choice('abcdefghijklmnop') for i in range(16))

    return ret
