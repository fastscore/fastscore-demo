# fastscore.recordsets.0: true
# fastscore.recordsets.1: false
# fastscore.module-attached: nltk
# fastscore.module-attached: gensim

import pickle
import nltk
import gensim
import functools
import pandas as pd
import scipy
import sys

def remove_proper_nouns(string):
    list_of_words = string.split()
    tagged_low = nltk.tag.pos_tag(list_of_words)
    removed_proper_nouns = list(filter(lambda x: x[1] != 'NNP', tagged_low))
    untagged_low = list(map(lambda x: x[0], removed_proper_nouns))
    return " ".join(untagged_low)

def preprocess(series):

    removed_proper_nouns = series.astype(str).apply(remove_proper_nouns)
    CUSTOM_FILTERS = [lambda x: x.lower(), 
                      gensim.parsing.preprocessing.strip_tags, 
                      gensim.parsing.preprocessing.strip_punctuation]

    preprocessing = gensim.parsing.preprocess_string
    preprocessing_filters = functools.partial(preprocessing, filters=CUSTOM_FILTERS)
    removed_punctuation = removed_proper_nouns.apply(preprocessing)

    stopword_remover = gensim.parsing.preprocessing.remove_stopwords
    stopword_remover_list = lambda x: list(map(stopword_remover, x))
    cleaned = removed_punctuation.apply(stopword_remover_list)

    filter_short_words = lambda x: list(filter(lambda y: len(y) > 1, x))
    cleaned = cleaned.apply(filter_short_words)

    filter_non_alpha = lambda x: list(filter(lambda y: y.isalpha(), x))
    cleaned = cleaned.apply(filter_non_alpha)
    
    stemmer = nltk.stem.porter.PorterStemmer()
    list_stemmer = lambda x: list(map(lambda y: stemmer.stem(y), x))
    cleaned = cleaned.apply(list_stemmer)

    return cleaned

def pad_sparse_matrix(sp_mat, length, width):
    sp_data = (sp_mat.data, sp_mat.indices, sp_mat.indptr)
    padded = scipy.sparse.csr_matrix(sp_data, shape=(length, width))
    return padded


def begin():
    global lasso_model_artifacts 
    lasso_model_artifacts = pickle.load(open('/fastscore/lasso_model_artifacts.pkl', 'rb'))
    pass

def action(x):
    lasso_model = lasso_model_artifacts['lasso_model']
    dictionary = lasso_model_artifacts['dictionary']
    threshold = lasso_model_artifacts['threshold']
    tfidf_model = lasso_model_artifacts['tfidf_model']
    
    cleaned = preprocess(x.content)
    corpus = cleaned.apply(dictionary.doc2bow)
    corpus_sparse = gensim.matutils.corpus2csc(corpus).transpose()
    corpus_sparse_padded = pad_sparse_matrix(sp_mat = corpus_sparse, 
                                             length=corpus_sparse.shape[0], 
                                             width = len(dictionary))
    sys.stdout.flush()
    tfidf_vectors = tfidf_model.transform(corpus_sparse_padded)

    probabilities = lasso_model.predict_proba(tfidf_vectors)[:,1]

    predictions = pd.Series(probabilities > threshold, index=x.index).astype(int)
    output = pd.concat([x, predictions], axis=1)
    output.columns = ['content', 'id', 'prediction']
    # yield output
    yield output.to_dict(orient="records")

