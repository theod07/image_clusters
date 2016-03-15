import pandas as pd
import numpy as np
import cPickle
import download_imgs as dl
import random
# from vgg16_model import model as nn


def rand_samp(items, k=100):
    if len(items) <= k:
        return items
    else:
        return random.sample(items, k)

if __name__ == '__main__':

    usernames = ['year', 'oceana', 'paolatonight', 'patricknorton']

    for username in usernames:
        src_urls = dl.get_src_urls(username)
        src_urls_samp = rand_samp(src_urls)
        preds = []

        for url in src_urls_samp:
            #simulate a prediction
            pred = np.random.rand(1000)
            # pred = nn.predict(url)[0]
            preds.append(pred)

        df = pd.DataFrame(zip(src_urls_samp, preds), columns=['src_url','prediction'])
        fname = '../data/{}/{}_predictions.pkl'.format(username, username)
        df.to_pickle(fname)
        with open('../logs/log_dataframe.txt', 'ab') as f:
            f.write('dataframe saved to {}'.format(fname))
        print 'dataframe saved to {}'.format(fname)
