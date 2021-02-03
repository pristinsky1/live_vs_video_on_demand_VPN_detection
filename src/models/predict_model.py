'''
predict_model.py is used to predict an web activity is generated using vpn or not using trained model.
'''
## import library
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from scipy.signal import find_peaks 
import pickle
import os
import json 
from sklearn.metrics import confusion_matrix
from ..data.etl import clean_data
from ..data.etl import generate_info
from ..features.build_features import main_import

def predict_model(indir,indir2, outdir):
    '''
    return two table contains predictions of each test data and analysis.
    :param: indir: file directory where trained model stored
    :param: indir2: file directory where test data stored
    :param: outdir: file directory where generated predictions stored
    '''
    filename = os.path.join(indir, 'model.joblib')
    loaded_model = pickle.load(open(filename, 'rb'))
    df = main_import(indir2,outdir,0)
    df2 = df[['2->1Bytes.spike_count','2->1Bytes.spike_mean']].dropna()
    predictions = loaded_model.predict(df2)
    df=df.dropna(subset=['2->1Bytes.spike_count','2->1Bytes.spike_mean'])
    df=df[['username','video/novideo','streaming_provider','quality','playback_speed','vpn/novpn','platform',\
                 'clean/noisy','date','#split']]
    predictions=['video' if i==1 else 'novideo' for i in predictions ]
    df['predictions']=predictions
    df.to_csv (outdir+'/predictions.csv', index = False, header=True)
    y_true=[1 if i=="video" else 0 for i in df['video/novideo']]
    y_pred=[1 if i=="video" else 0 for i in df['predictions']]
    model_report={}
    model_report["Using Features"]='2->1Bytes.spike_count, 2->1Bytes.spike_mean'
    model_report["Test Accuracy"]= str(balanced_accuracy_score(y_true,y_pred))
    tn, fp, fn, tp = confusion_matrix(y_true,y_pred).ravel()
    model_report["True Negative"]=str(tn)
    model_report["False Positive"]=str(fp)
    model_report["False Negative"]=str(fn)
    model_report["True Positive"]=str(tp)
    filename2 = os.path.join(outdir, 'test_report.json')
    with open(filename2, "w") as outfile:  
        json.dump(model_report, outfile)
    