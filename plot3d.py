# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 14:36:39 2021

@author: valer
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from mpl_toolkits import mplot3d

def plot3d(data,titre,n_lignes=None):
    fig = plt.figure()
    fig.suptitle(titre)
    ax = fig.add_subplot(111, projection='3d')
    if n_lignes==None:
        ax.scatter(data[:,0],data[:,1],data[:,2],cmap='bwr',alpha=1)
    else:
        ax.scatter(data[:n_lignes,0],data[:n_lignes,1],data[:n_lignes,2],cmap='bwr',alpha=1)
    ax.set_xlabel('aggressiveness')
    ax.set_ylabel('visibility')
    ax.set_zlabel('danger')
    ax.invert_yaxis()
    plt.show()
    
df = pd.read_csv('data/cleaned/clean5.csv',sep=",")

df_id = df.iloc[:,0]
df = df.drop(axis=1,index=0)

scaler = StandardScaler()
scaled_df = scaler.fit_transform(df)
pca = PCA(n_components=3).fit_transform(scaled_df)



plot3d(pca,"données")