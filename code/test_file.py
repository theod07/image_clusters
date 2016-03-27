import os
from vgg16_model import vgg16_gpu
from vgg16_model import vgg16_cpu
from vgg16_model.model import prep_image, predict
import cPickle as pickle
import numpy as np
import lasagne

model = pickle.load(open('./vgg16_model/vgg16.pkl'))
CLASSES = model['synset words']
MEAN_IMAGE = model['mean value'][:, np.newaxis, np.newaxis] # necessary to match dimensions of incoming images

nnet_gpu = vgg16_gpu.build_model()
nnet_cpu = vgg16_cpu.build_model()


if __name__ == '__main__':

	GPU = False

	if GPU:
		nnet = nnet_gpu.copy()
	else: 
		nnet = nnet_cpu.copy()

	lasagne.layers.set_all_param_values(nnet['prob'], model['param values'])

	imgs = [ f for f in os.listdir('.') if f.endswith('.jpg') ]

	for img in imgs:
		prob = predict(img, local_img=True)
