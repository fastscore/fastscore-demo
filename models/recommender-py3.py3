# fastscore.schema.0: input
# fastscore.schema.1: output

# fastscore.module-attached: autorecommender
from autorecommender.models.autoencoder import load_model
from autorecommender.data import Dataset, ratings_matrix_to_list

import pandas as pd
import numpy as np
import sys

def begin():
    global movies, model
    movies = pd.read_csv("/fastscore/datasets/movies.csv")
    model = load_model("/fastscore/artifacts/autorecommender.zip")
    print("MODEL LOADED")
    sys.stdout.flush()

def action(ratings):
    rows = [{"userid": 0, "movieid": int(x), "rating": ratings[x]} for x in ratings]
    ratings_list = pd.DataFrame(rows).set_index(["userid", "movieid"])
    predictions = model.predict(ratings_list)
    films = movies.iloc[predictions.transpose().sort_values(by=0, ascending=False).iloc[0:10].index]
    yield list(films["title"])
