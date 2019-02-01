# fastscore.schema.0: ratings
# fastscore.schema.1: output
# fastscore.module-attached: autorecommender

from autorecommender.models.autoencoder import load_model

def begin():
    global trained_model, STOCKS, STOCKS_TICKER_LOOKUP
    trained_model = load_model('model.zip')
    
    DATA_PATH = '' # Update this if necessary
    STOCKS_CSV = DATA_PATH + 'stocks.csv'

    STOCKS = pd.read_csv(STOCKS_CSV)
    STOCKS = STOCKS.set_index('stockid').sort_index()

    STOCKS_TICKER_LOOKUP = STOCKS.reset_index().set_index('ticker')

def df_from_fastscore(x):
    userid = x['userid']
    ratings_list = []
    for r in x['ratings']:
        key = list(r.keys())[0]
        val = list(r.values())[0]
        ratings_list.append({'userid': userid, 
                             'stockid': STOCKS_TICKER_LOOKUP.loc[key]['stockid'].iloc[0], 
                             'rating' : val})
    return pd.DataFrame(ratings_list).set_index(['userid', 'stockid'])
    
def predictions_to_recommendations(preds, userid):
    stockids = preds.transpose().sort_values(by=userid, ascending=False).index[0:10]
    outs = [stockid_to_stockname(x) for x in stockids]
    return outs

def stockid_to_stockname(number):
    x = STOCKS.loc[number]
    return x['ticker']

def action(x):
    userid = x['userid']
    inputs = df_from_fastscore(x)
    yield predictions_to_recommendations(trained_model.predict(inputs), userid)
