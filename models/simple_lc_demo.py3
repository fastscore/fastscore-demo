import pandas as pd
import numpy
import scipy
import sys as sys

from sklearn.metrics import confusion_matrix, f1_score, roc_curve, auc

def begin():
    global features, model_coefs, thresh
    features = ['log_loan_amnt', 'log_int_rate', 'log_age_of_earliest_cr_line',
                'log_annual_inc', 'rent', 'own']

    if 'dti' in features:
        model_coefs = {'log_loan_amnt': 0.10515290398859556,
                       'log_int_rate': 1.4125530012492467,
                       'log_age_of_earliest_cr_line': 0.008318491200831423,
                       'log_annual_inc': -0.48319162538438015,
                       'rent': 0.1990104609638132,
                       'own': 0.11828020505700797,
                       'dti': 0.010780961456227825,
                       'intercept': 0.31729066601701106}
        thresh = 0.6222736560023592
    else:
        model_coefs = {'log_loan_amnt': 0.12220459449094405,
                       'log_int_rate': 1.4458733653799867,
                       'log_age_of_earliest_cr_line': 0.03671337711049522,
                       'log_annual_inc': -0.5330770627366136,
                       'rent': 0.31076743178543875,
                       'own': 0.23713770101322726,
                       'intercept': 0.5479051328012445}

        thresh = 0.6211685845208699
    pass

def action(datum):
    score = sum([datum[feat] * model_coefs[feat] for feat in features])
    score += model_coefs['intercept']
    pred_proba = scipy.special.expit(score)
    sys.stdout.flush()
    print("Predicted probability: " + str(pred_proba));
    if pred_proba > thresh: yield "Default"
    else: yield "Pay Off"

def backtest(data):
    actuals = data.loan_status
    data['intercept'] = 1
    coef_list = list(model_coefs.values())
    cols = features + ['intercept']
    scores = numpy.dot(data.loc[:,cols].values, numpy.array(coef_list))
    pred_proba = pd.Series(scipy.special.expit(scores))
    pred_classes = pred_proba.apply(lambda x: x > thresh).astype(int)

    cm = confusion_matrix(actuals, pred_classes)
    f1 = f1_score(actuals, pred_classes)
    fpr, tpr, threshold = roc_curve(actuals,pred_proba)
    auc_val = auc(fpr, tpr)
    classes = ['Pay Off', 'Default']
    yield dict(confusion_matrix = cm_to_dict(cm, classes),
               f1 = f1,
               roc = tpr_fpr_roc(fpr, tpr),
               auc = auc_val)

def cm_to_dict(cm, classes):
    out = []
    for idx, cl in enumerate(classes):
        out.append(dict(zip(classes, cm[idx,:].tolist())))
    return out

def tpr_fpr_roc(fpr, tpr):
    dict_of_trpfrp = dict(fpr=fpr.tolist(), tpr = tpr.tolist())
    lofd = [dict(zip(dict_of_trpfrp, t)) for t in zip(*dict_of_trpfrp.values())]
    return lofd
