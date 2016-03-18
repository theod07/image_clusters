import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

def get_photos_df():
    pickles = os.listdir('../pickles')
    dfs = []
    for pickle in pickles:
        username = pickle.split('_predictions.pkl')[0]
        df = pd.read_pickle('../pickles/{}'.format(pickle))
        df['username'] = username
        dfs.append(df)
    return pd.concat(dfs, axis=0, ignore_index=True)

def get_users_df(photos_df):
    pickles = os.listdir('../pickles')
    dfs = []
    for pickle in pickles:
        username = pickle.split('_predictions.pkl')[0]
        df = pd.read_pickle('../pickles/{}'.format(pickle))
        vecs = np.zeros([df.shape[0], 1000])
        for row in range(df.shape[0]):
            vecs[row,:] = df.


    return
if __name__ == '__main__':
    sns.set(style="white", context="talk")

    photos_df = get_photos_df()
    users_df = get_users_df()
    usernames = pd.unique(photos_df.username)

    photos_mat = np.zeros([photos_df.shape[0], 1000])
    for row in range(photos_df.shape[0]):
        photos_mat[row,:] = photos_df.prediction[row]

    u,s,v = np.linalg.svd(photos_mat)

    energy = s**2
    cum_energy = np.cumsum(energy)
    norm_cum_energy = cum_energy / cum_energy[-1]
    # print cum_energy[:10]
    # norm_cum_energy[294]  >>>>>  0.90047322651909756
    # norm_cum_energy[293]  >>>>>  0.89972063768911648

    # plt.plot(norm_cum_energy)
    # plt.title('normalized cumulative energy\n (43 users, 100img/user)')
    # plt.hlines(.9,0,1000)
    # plt.show()
