import os
from vgg16_model import vgg16
from vgg16_model import vgg16_cpu
from vgg16_model import model
import cPickle as pickle
import numpy as np

model = pickle.load(open('./vgg16_model/vgg16.pkl'))
CLASSES = model['synset words']
MEAN_IMAGE = model['mean value'][:, np.newaxis, np.newaxis] # necessary to match dimensions of incoming images

nnet = vgg16.build_model()
# nnet = vgg16_cpu.build_model()

lasagne.layers.set_all_param_values(nnet['prob'], model['param values'])



imgs = ['natgeo_10009268_740227179454995_1126758630_n.jpg',
		'natgeo_10009414_871221042997178_322070705_n.jpg', 
		'natgeo_10011420_443055039211825_611359185_n.jpg',
		'natgeo_10011514_463266313865771_1194066775_n.jpg', 
		'natgeo_10175197_1537119106600073_1792863643_n.jpg',
		'natgeo_10175373_1701735806739918_820309524_n.jpg']

for img in imgs:
	model.predict('../imgs/{}'.format(img), local_img=True)

