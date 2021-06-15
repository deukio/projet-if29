# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 15:11:00 2021

@author: valer
"""
import os
import json
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# def main():
df = pd.read_csv('data/cleaned/clean0.csv',sep=",")
    
df_id = df.iloc[:,0]
df = df.drop(df.columns[0],axis=1)

scaler = StandardScaler()
scaled_df = scaler.fit_transform(df)
df_pca = PCA(n_components=3).fit_transform(scaled_df)

km = KMeans(2,n_jobs=-1).fit_predict(df_pca)

def lookFor(userid):
    path = "C:/Users/valer/.spyder-py3/IF29/projet/data/raw"
    for filename in os.listdir(path):
        with open(path+"/"+filename,encoding='UTF-8') as file:
            for tweet in (json.loads(line) for line in file):
                if tweet['user']['id'] == userid:
                    return tweet['text'],tweet['user']['friends_count'],tweet['user']['created_at']

