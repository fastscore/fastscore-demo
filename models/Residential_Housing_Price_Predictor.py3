import numpy
import pickle
import pandas as pd


# modelop.init
def begin():
    global xgb_model, means, stdevs, shap_explainer, garageyrbuilt_mean, features

    artifacts = pickle.load(open('/fastscore/xgb_shap_artifacts.pkl','rb'))
    xgb_model = artifacts['xgb_model']
    shap_explainer = artifacts['shap_explainer']
    means = artifacts['means']
    stdevs = artifacts['stdevs']
    garageyrbuilt_mean = artifacts['garageyrbuilt_mean'] #Used for imputing a missing
    features = artifacts['features'] #XGBoost is finicky about order
    pass


# modelop.score
def action(datum):
    standard_datum = datum
    for k in means.keys():
        standard_datum[k] = (datum[k] - means[k]) / stdevs[k]

    if not datum['GarageYrBlt']:
        datum['GarageYrBlt'] = garageyrbuilt_mean

    idx = standard_datum.pop("Id")

    pd_datum = pd.DataFrame(standard_datum, index=[idx], columns = features)
    prediction_raw = xgb_model.predict(pd_datum)[0]
    prediction = numpy.exp(prediction_raw)

    shap_values = shap_explainer.shap_values(pd_datum.values)[0]
    shap_values = pd.Series(shap_values, index=features)

    yield dict(Id = idx, xgboost_pred = prediction, shap_values=shap_values.to_dict())
