# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 14:53:16 2021

@author: valer
"""
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 10:23:43 2021

@author: valer
"""

import csv
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
from matplotlib import pyplot as plt
import cProfile
import pstats
import functools
from tqdm import tqdm
from sklearn.metrics import silhouette_samples, silhouette_score

# def main():
df = pd.read_csv('data/cleaned/clean0.csv',sep=",")
    

scaler = StandardScaler()
df = scaler.fit_transform(df)
pca = PCA(n_components=0.9,svd_solver='full').fit(df)

df_pca = pca.transform(df)

def plotCluster(start,stop):
    inertia=[]
    fig, ax = plt.subplots(1,stop-start+2)
    for index,n_clusters in enumerate(range(start,stop+1)):
        km = KMeans(n_clusters=n_clusters,n_jobs=-1,n_init=5,max_iter=100)
        km = km.fit(df_pca)
        clusters = km.predict(df_pca)
        inertia.append(km.inertia_)
        silhouette_vals = silhouette_samples(df_pca,clusters)
        
        # Silhouette plot
        y_ticks = []
        y_lower, y_upper = 0, 0
        for i, cluster in enumerate(np.unique(clusters)):
            cluster_silhouette_vals = silhouette_vals[clusters == cluster]
            cluster_silhouette_vals.sort()
            y_upper += len(cluster_silhouette_vals)
            ax[index].barh(range(y_lower, y_upper), cluster_silhouette_vals, edgecolor='none', height=1)
            ax[index].text(-0.03, (y_lower + y_upper) / 2, str(i + 1))
            y_lower += len(cluster_silhouette_vals)
    
        # Get the average silhouette score and plot it
        avg_score = np.mean(silhouette_vals)
        ax[index].axvline(avg_score, linestyle='--', linewidth=2, color='green')
        ax[index].set_yticks([])
        ax[index].set_xlim([-0.1, 1])
        ax[index].set_xlabel('Silhouette coefficient values')
        ax[index].set_ylabel('Cluster labels')
        ax[index].set_title('{} clusters'.format(cluster), y=1.02)
        
    ax[stop-start+1].plot(list(range(start,stop+1)),inertia,'-o')

def plotInertia(start,stop):
    inertia=[]
    for index,n_clusters in enumerate(range(start,stop+1)):
        km = KMeans(n_clusters=n_clusters,n_jobs=-1,n_init=5,max_iter=100)
        km = km.fit(df_pca)
        inertia.append(km.inertia_)
    plt.plot(list(range(start,stop+1)),inertia,'-o')

# def profiler(func):
#     cProfile.run(func,'{}.profile'.format(func))
#     stats = pstats.Stats('{}.profile'.format(func))
#     stats.strip_dirs().sort_stats('time').print_stats()
    
# profiler('main()')