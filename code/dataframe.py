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
    if fname in os.listdir('../pickles/'.format(user)):
        return True
    return False

def load_pkl(user):
    fname = '../pickles/{}_predictions.pkl'.format(user)
    df = cPickle.load(open(fname, 'rb'))
    print 'columns in df for {}: {}'.format(user, df.columns
    # desired_cols = set(['username', 'shortcode', 'src_url', 'prediction'])
    # cur_cols = set(df.columns)
    # new_cols = desired_cols - cur_cols
    # while new_cols:
    #     df['{}'.format(new_cols.pop())] = 'null'
    return df


if __name__ == '__main__':

    # users = ['year', 'oceana', 'paolatonight', 'patricknorton']
    # users = ['jamieoliver', 'solar', 'trey5', 'worthwhilestyle', 'toppeopleworld', 'nycmayorsoffice', 'jessicaalba', 'toms', 'walaad', 'starbucks', 'warbyparker', 'theultimateclub', 'victoriassecret', 'jeremymcgrath2', 'julian_wilson', 'wired', 'taylorswift', 'skinart_mag', 'theroxy', 'twheat', 'laurenconrad', 'letthelordbewithyou', 'nickkristof']
    users = ['patricknorton']

    for user in users:
        if has_predictions_pkl(user):
            df1 = load_pkl(user)
            print 'previous df shape: {}'.format(df1.shape)

            all_src_urls = set(dl.get_src_urls(user))
            cur_src_urls = set(df1.src_url)
            src_urls_toadd = all_src_urls - cur_src_urls
            df2 = pd.Series(list(src_urls_toadd))
            merged_df = pd.concat([df1, df2], axis=0)

            print 'new df shape: {}'.format(merged_df.shape)
            fname = '../pickles/{}_predictions.pkl'.format(user)
            merged_df.to_pickle(fname)


    # for user in users:
    #     src_urls = dl.get_src_urls(user)
    #     src_urls_samp = rand_samp(src_urls)
    #     preds = []
    #
    #     for url in src_urls_samp:
    #         #simulate a prediction
    #         # pred = np.random.rand(1000)
    #         pred = nn.predict(url)[0]
    #         preds.append(pred)
    #
    #     df = pd.DataFrame(zip(src_urls_samp, preds), columns=['src_url','prediction'])
    #     fname = '../pickles/{}_predictions.pkl'.format(user)
    #     df.to_pickle(fname)
    #     with open('../logs/log_dataframe.txt', 'ab') as f:
    #         f.write('{} dataframe saved to {}\n'.format(strftime('%Y%m%d.%H:%M:%s'), fname))
    #     print '{} dataframe saved to {}\n'.format(strftime('%Y%m%d.%H:%M:%s'), fname)
