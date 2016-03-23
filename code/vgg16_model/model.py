import lasagne
from lasagne.layers import InputLayer
from lasagne.layers import DenseLayer
from lasagne.layers import NonlinearityLayer
from lasagne.layers import DropoutLayer
from lasagne.layers import Pool2DLayer as PoolLayer
from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.nonlinearities import softmax
from lasagne.utils import floatX
import numpy as np
import pickle
import vgg16
import urllib
import io
import skimage.transform
import matplotlib.pyplot as plt
import time
# import matplotlib
# matplotlib.use('agg')

model = pickle.load(open('./vgg16_model/vgg16.pkl'))
CLASSES = model['synset words']
MEAN_IMAGE = model['mean value'][:, np.newaxis, np.newaxis] # necessary to match dimensions of incoming images

nnet = vgg16.build_model()

lasagne.layers.set_all_param_values(nnet['prob'], model['param values'])


index = urllib.urlopen('http://www.image-net.org/challenges/LSVRC/2012/ori_urls/indexval.html').read()
image_urls = index.split('<br>')

np.random.seed(23)
np.random.shuffle(image_urls)
# image_urls = image_urls[:20]

def prep_image(img_path, nnet=nnet, local_img=True):
    ext = img_path.split('.')[-1]

    if local_img:
        im = plt.imread(img_path)
    else:
        im = plt.imread(io.BytesIO(urllib.urlopen(img_path).read()), ext)

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

def predict(img_path, local_img=True):
    try:
        tic = time.clock()
        print 'tic'
        rawim, im = prep_image(img_path, local_img)
        print 'prepped'
        print 'calculating probs..'
        prob = np.array(lasagne.layers.get_output(nnet['prob'], im, deterministic=True).eval())
        print 'got probs..'
        top = np.argsort(prob[0])[-1:-4:-1]
        # print 'preparing to plot'
        # plt.figure()
        # plt.imshow(rawim.astype('uint8'))
        # plt.axis('off')
        # print 'successfully plotted'
        toc = time.clock()

        print "img_path: {}".format(img_path)
        print "predict time: {}".format(toc-tic)
        for n, label in enumerate(top):
            # plt.text(250, 70 + n * 20, '{}. {}'.format(n+1, CLASSES[label]), fontsize=14)
            print '{}.  Class: {}.'.format(n+1, CLASSES[label])
    # except IOError:
    except:
        print('bad img_path: ' + img_path)
        return np.zeros(1000)
    return prob

if __name__ == '__main__':

    sample_size = 2

    with open('../../data/EXAMPLE_taylorswift/EXAMPLE_taylorswift_src_urls.txt', 'r') as f:
        lines = f.readlines()
        image_urls = [line.split('\n')[0] for line in lines]

    urls = image_urls[:sample_size]
    probs = []
    while len(urls) > 0:
        probs.append(predict(urls.pop()))
