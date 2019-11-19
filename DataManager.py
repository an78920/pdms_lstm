import PIWebAPI as piapi
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import math

#endpoint = 'https://192.168.10.12/piwebapi'
endpoint = 'https://project.iiotfab.com/piwebapi'
piserver = 'PI-IDES'
user = 'piuser'
password = 'piuser'


def getPIData(tag, startTime, endTime):
    webid = piapi.get_webid(endpoint, user, password, piserver, tag)
    summary = piapi.GetSummary(endpoint, user, password, webid)
    summary.startTime = startTime
    summary.endTime = endTime
    summary.summaryDuration = '5m'
    summary.summaryType = 'Total'

    jdata = summary.query()
    print(summary.url)

    data = json_normalize(jdata['Items'], max_level=2)[['Value.Timestamp', 'Value.Value']]
    data.columns = ['Timestamp', 'Value']
    data.Value = data.Value * 86400

    return data


def addFeature(train):
    train.index = pd.to_datetime(train.Timestamp) + pd.DateOffset(hours=8)
    train = train.drop('Timestamp', axis=1)

    #train['Timestamp'] = pd.to_datetime(train['Timestamp']) + pd.DateOffset(hours=8)

    train['Day'] = train.index.dayofweek + 1
    train['Hour'] = train.index.hour
    train['IsWork'] = [1 if (i >= 9) & (i <= 18) else 0 for i in train['Hour']]

    return train


def normalize(train):
    train['Value'] = np.log(train['Value'] + 1)

    return train


def buildTrain(train, pastStep=30, futureStep=5):
    X_train, Y_train = [], []
    for i in range(train.shape[0] - futureStep - pastStep):
        X_train.append(np.array(train.iloc[i:i + pastStep]))
        Y_train.append(np.array(train.iloc[i + pastStep:i + pastStep + futureStep]['Value']))

    return np.array(X_train), np.array(Y_train)


def splitData(X, Y, rate):
    X_train = X[int(X.shape[0] * rate):]
    Y_train = Y[int(Y.shape[0] * rate):]
    X_val = X[:int(X.shape[0] * rate)]
    Y_val = Y[:int(Y.shape[0] * rate)]
    return X_train, Y_train, X_val, Y_val


def multi(test):
    a = 1
    for i in test:
        a *= i

    return -math.log(a)