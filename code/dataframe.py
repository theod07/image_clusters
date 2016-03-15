import pandas as pd
import numpy as np
import cPickle
import download_imgs as dl
import random
import os
from time import strftime
# from vgg16_model import model as nn

def rand_samp(items, k=100):
    if len(items) <= k:
        return items
    else:
        return random.sample(items, k)

def has_predictions_pkl(user):
    fname = '{}_predictions.pkl'.format(user)
    if fname in os.listdir('../data/{}/'.format(user)):
        return True
    return False

if __name__ == '__main__':

    users = ['year', 'oceana', 'paolatonight', 'patricknorton']

    for user in users:
        src_urls = dl.get_src_urls(user)
        src_urls_samp = rand_samp(src_urls)
        preds = []

        for url in src_urls_samp:
            #simulate a prediction
            pred = np.random.rand(1000)
            # pred = nn.predict(url)[0]
            preds.append(pred)

        df = pd.DataFrame(zip(src_urls_samp, preds), columns=['src_url','prediction'])
        fname = '../data/{}/{}_predictions.pkl'.format(user, user)
        df.to_pickle(fname)
        with open('../logs/log_dataframe.txt', 'ab') as f:
            f.write('{} dataframe saved to {}'.format(strftime('%Y%m%d.%H:%M:%s'), fname))
        print '{} dataframe saved to {}'.format(strftime('%Y%m%d.%H:%M:%s'), fname)
