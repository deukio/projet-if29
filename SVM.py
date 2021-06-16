# -*- coding: utf-8 -*-
"""
Created on WEN Jun 16 17:05:07 2021
@author: VGuich
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from sklearn.svm import SVC
import seaborn as sns
import time

def plot3d(data,categorie,titre,n_lignes=None):
    fig = plt.figure()
    fig.suptitle(titre)
    ax = fig.add_subplot(111, projection='3d')
    if n_lignes==None:
        ax.scatter(data[:,0],data[:,3],data[:,1],c=categorie[:],cmap='bwr',alpha=1)
    else:
        ax.scatter(data[:n_lignes,0],data[:n_lignes,3],data[:n_lignes,1],c=categorie[:n_lignes],cmap='bwr',alpha=1)
    ax.set_xlabel('aggressiveness')
    ax.set_ylabel('spam')
    ax.set_zlabel('danger')
    ax.invert_yaxis()
    plt.show()
    
# def main():
df = pd.read_csv('data/cleaned/clean0.csv',sep=",")
    
df_id = df.iloc[:,0]
df = df.drop(df.columns[0],axis=1)

scaler = StandardScaler()
scaled_df = scaler.fit_transform(df)
df_pca = PCA(n_components=3).fit_transform(scaled_df)

km = KMeans(2,n_jobs=-1).fit_predict(df_pca)

print("\nSVM:")
X_train, X_test, y_train, y_test = train_test_split(scaled_df, km, test_size=0.30)

svm = SVC(random_state=42)
svm.fit(X_train[:],y_train[:])

prd = svm.predict(X_test)
prd2 = svm.predict(scaled_df)
plot3d(scaled_df,prd2,"SVM")



