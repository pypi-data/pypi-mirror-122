import pandas as pd
import numpy as np
import glob
import os
import bson
import multiprocessing
import seaborn as sns
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

def df_for_ML(df):
    df = df.fillna(0)
    modified_df = df
    modified_df.insert(0, 'New_ID', range(1, 1 + len(df)))
    aux_df = modified_df[['New_ID', 'hm_t_gol']]
    aux_df['New_new_ID'] = aux_df['New_ID'] - 1
    aux_df.drop(['New_ID'], inplace=True, axis=1)
    aux_df.columns = ['hm_t_gol_pred', 'New_new_ID']
    ML_df = pd.merge(modified_df, aux_df, how='inner', left_on=['New_ID'], right_on=['New_new_ID'])
    ML_df = ML_df.select_dtypes(include=['float64', 'int']).fillna(0)

    return (ML_df)

def ML_random_forest(df):
    model = RandomForestClassifier(max_depth=200, random_state=0)
    c1y = df['hm_t_gol_pred']
    c1x = df.drop(['hm_t_gol_pred'], axis=1)
    x_train, x_test, y_train, y_test = train_test_split(c1x, c1y, test_size=0.2, random_state=42)
    y_predict = model.fit(x_train, y_train).predict(x_test)
    print(classification_report(y_test, y_predict))
    print(confusion_matrix(y_test, y_predict))