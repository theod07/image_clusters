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

def get_users_df():
    pickles = os.listdir('../pickles')
    usernames, user_vecs = [], []
    tp = type(np.zeros(1000))

    for pickle in pickles:
        username = pickle.split('_predictions.pkl')[0]
        df = pd.read_pickle('../pickles/{}'.format(pickle))
        try:
            # vecs = [df.prediction[row] for row in range(df.shape[0]) if df.prediction[row].shape[0] == 1000]
            # photos that were unable to be calculated were returned as float, not numpy.ndarray
            vecs = [df.prediction[row] for row in range(df.shape[0]) if type(df.prediction[row]) == tp]
            vecs = np.array(vecs)
        except KeyError:
            df = df.reset_index()
            # vecs = [df.prediction[row] for row in range(df.shape[0]) if df.prediction[row].shape[0] == 1000]
            # photos that were unable to be calculated were returned as float, not numpy.ndarray
            vecs = [df.prediction[row] for row in range(df.shape[0]) if type(df.prediction[row]) == tp]
            vecs = np.array(vecs)
        print '{} vecs.shape: {}'.format(username, vecs.shape)

        usernames.append(username)
        user_vecs.append(np.mean(vecs, axis=0))

    usernames = np.array(usernames)
    user_mat = np.array(user_vecs)
    return usernames, user_mat

if __name__ == '__main__':
    sns.set(style="white", context="talk")

    photos_df = get_photos_df()
    users_df = get_users_df()
    usernames = pd.unique(photos_df.username)

    photos_mat = np.zeros([photos_df.shape[0], 1000])
    for row in range(photos_df.shape[0]):
        photos_mat[row,:] = photos_df.prediction[row]

    u,s,v = np.linalg.svd(photos_mat)

    photos_energy = s**2
    photos_cum_energy = np.cumsum(photos_energy)
    photos_norm_cum_energy = photos_cum_energy / photos_cum_energy[-1]
    # print photos_cum_energy[:10]
    # photos_norm_cum_energy[294]  >>>>>  0.90047322651909756
    # photos_norm_cum_energy[293]  >>>>>  0.89972063768911648

    # plt.plot(photos_norm_cum_energy)
    # plt.title('normalized cumulative photos_energy\n (43 users, 100img/user)')
    # plt.hlines(.9,0,1000)
    # plt.show()

    usernames, users_mat = get_users_df()
    u,s,v = np.linalg.svd(users_mat)

    users_energy = s**2
    users_cum_energy = np.cumsum(users_energy)
    users_norm_cum_energy = users_cum_energy / users_cum_energy[-1]
    # s.shape  >>>>> (42,)

    print users_norm_cum_energy[users_norm_cum_energy > 0.9]
    plt.plot(users_norm_cum_energy)
    plt.title('normalized cumulative users_energy\n (43 users, 100img/user)')
    plt.hlines(.9,0,1000)
    plt.show()
