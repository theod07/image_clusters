import pandas as pd
import numpy as np
import cPickle
import download_imgs as dl
import random
import time
def rand_samp(items, k=100):
    if len(items) <= k:
        return items
    else:
        return random.sample(items, k)

username = 'year'
src_urls = dl.get_src_urls(username)
src_urls_samp = rand_samp(src_urls)

deltas = []
for i in xrange(5000):
    tic = time.clock()
    preds = []
    for i in xrange(1000):
        #simulate a prediction
        prediction = np.random.rand(1000)
        preds.append(prediction)
    toc = time.clock()
    # print 'delta: {}'.format(toc-tic)
    deltas.append(toc-tic)
print 'mean delta (list): {}'.format(np.mean(deltas))

deltas = []
for i in xrange(5000):
    tic = time.clock()
    preds = np.zeros([1000,1000])
    for i in xrange(1000):
        #simulate a prediction
        prediction = np.random.rand(1000)
        preds[i,:] = prediction
    toc = time.clock()
    deltas.append(toc-tic)
print 'mean delta (numpy): {}'.format(np.mean(deltas))
