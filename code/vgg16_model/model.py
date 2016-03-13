import numpy as np
import lasagne
from lasagne.layers import InputLayer
from lasagne.layers import DenseLayer
from lasagne.layers import NonlinearityLayer
from lasagne.layers import DropoutLayer
from lasagne.layers import Pool2DLayer as PoolLayer
from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.nonlinearities import softmax
from lasagne.utils import floatX
import pickle
import vgg16
import urllib
import io
import skimage.transform
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('agg')

model = pickle.load(open('vgg16.pkl'))
CLASSES = model['synset words']
MEAN_IMAGE = model['mean value'][:, np.newaxis, np.newaxis] # necessary to match dimensions of incoming images

nnet = vgg16.build_model()

lasagne.layers.set_all_param_values(nnet['prob'], model['param values'])


index = urllib.urlopen('http://www.image-net.org/challenges/LSVRC/2012/ori_urls/indexval.html').read()
image_urls = index.split('<br>')

np.random.seed(23)
np.random.shuffle(image_urls)
# image_urls = image_urls[:20]

def prep_image(url):
    ext = url.split('.')[-1]
    im = plt.imread(io.BytesIO(urllib.urlopen(url).read()), ext)
    # Resize so smallest dim = 256, preserving aspect ratio
    h, w, _ = im.shape
    if h < w:
        im = skimage.transform.resize(im, (256, w*256/h), preserve_range=True)
    else:
        im = skimage.transform.resize(im, (h*256/w, 256), preserve_range=True)

    # Central crop to 224x224
    h, w, _ = im.shape
    im = im[h//2-112:h//2+112, w//2-112:w//2+112]

    rawim = np.copy(im).astype('uint8')

    # Shuffle axes to c01
    im = np.swapaxes(np.swapaxes(im, 1, 2), 0, 1)

    # Convert to BGR
    im = im[::-1, :, :]

    im = im - MEAN_IMAGE
    return rawim, floatX(im[np.newaxis])


with open('../../data/zooeydeschanel/zooeydeschanel_src_urls.txt', 'r') as f:
    lines = f.readlines()
    image_urls = [line.split('\n')[0] for line in lines]


probs = []
for url in image_urls[:5]:
    try:
        rawim, im = prep_image(url)
        print 'calculating probs..'
        prob = np.array(lasagne.layers.get_output(nnet['prob'], im, deterministic=True).eval())
        probs.append(prob)
        print 'got probs..'
        top20 = np.argsort(prob[0])[-1:-21:-1]
        # print 'preparing to plot'
        # plt.figure()
        # plt.imshow(rawim.astype('uint8'))
        # plt.axis('off')
        # print 'successfully plotted'

        print "url: {}".format(url)
        for n, label in enumerate(top20):
            # plt.text(250, 70 + n * 20, '{}. {}'.format(n+1, CLASSES[label]), fontsize=14)
            print 'n+1: {}.  Class: {}.'.format(n+1, CLASSES[label])

    # except IOError:
    except:
        print('bad url: ' + url)
        probs.append('bad url')
