'''
predict_model.py is used to predict an web activity is generated using vpn or not using trained model.
'''
## import library
import pandas as pd
import os
import sys
from datetime import datetime
import numpy as np
from scipy.signal import find_peaks
from sklearn.metrics import accuracy_score
import sklearn.model_selection as model_selection
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import pickle
import json
from ..features.build_features import features_build


def predict_model(indir,indir2, outdir):
    '''
    return two table contains predictions of each test data and analysis.
    :param: indir: file directory where trained model stored
    :param: indir2: file directory where test data stored
    :param: outdir: file directory where generated predictions stored
    '''
    filename = os.path.join(indir, 'model.joblib')
    filename2 = os.path.join(indir, 'ori_table.csv')
    df2=pd.read_csv(filename2)
    loaded_model = pickle.load(open(filename, 'rb'))
    df = features_build(indir2,outdir,0)
    features_name = ["valid_package_rate","peaks_gap","peaks_number"]
    y = np.array(df["data_label"])
    x = np.array(df[features_name])
    predictions = loaded_model.predict(x)
    df['predictions']=predictions
    y_true=df['data_label']
    y_pred=df['predictions']
    df['data_label']=["live" if i == 1 else "streaming" for i in df['data_label']]
    df['predictions']=["live" if i == 1 else "streaming" for i in df['predictions']]
    df2['predictions']=df['predictions']
    df2.to_csv (outdir+'/predictions.csv', index = False, header=True)
    model_report={}
    model_report["Using Features"]='valid_package_rate, peaks_gap, peaks_number'
    model_report["Test Accuracy"]= str(accuracy_score(y_true,y_pred))
    tn, fp, fn, tp=0,0,0,0
    for i in np.arange(len(y_true)):
        if y_true[i]==0 and y_pred[i]==0:
            tn+=1
        if y_true[i]==1 and y_pred[i]==0:
            fp+=1
        if y_true[i]==0 and y_pred[i]==1:
            fn+=1
        if y_true[i]==1 and y_pred[i]==1:
            tp+=1
    model_report["Validation Set True Negative"]=str(tn)
    model_report["Validation Set False Positive"]=str(fp)
    model_report["Validation Set False Negative"]=str(fn)
    model_report["Validation Set True Positive"]=str(tp)
    filename2 = os.path.join(outdir, 'predict_report.json')
    with open(filename2, "w") as outfile:  
        json.dump(model_report, outfile)
    