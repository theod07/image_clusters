import os
# from vgg16_model import vgg16
from vgg16_model import vgg16_cpu
from vgg16_model import model

model = pickle.load(open('./vgg16_model/vgg16.pkl'))
CLASSES = model['synset words']
MEAN_IMAGE = model['mean value'][:, np.newaxis, np.newaxis] # necessary to match dimensions of incoming images

nnet = vgg16.build_model()
nnet_cpu = vgg16_cpu.build_model()

lasagne.layers.set_all_param_values(nnet['prob'], model['param values'])



imgs = os.listdir('../imgs/')[20]

for img in imgs:
	vgg16
