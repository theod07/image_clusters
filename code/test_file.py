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

	# GPU = False

	# if GPU:
	# 	nnet = nnet_gpu.copy()
	# else: 
	# 	nnet = nnet_cpu.copy()

	# lasagne.layers.set_all_param_values(nnet['prob'], model['param values'])

	imgs = [ f for f in os.listdir('.') if f.endswith('.jpg') ]

	# for img in imgs:
	# 	prob = predict(img, local_img=True)

	# GPU, sequential: 5.319, 3.318, 3.374, 3.358, 3.371, 3.381
	# CPU, sequential: 3.481, 3.396, 3.401, 3.378, 3.375, 3.404

	lasagne.layers.set_all_param_values(nnet_gpu['prob'], model['param values'])
	lasagne.layers.set_all_param_values(nnet_cpu['prob'], model['param values'])

	rawim, im = prep_image(imgs[0], local_img=True)

	prob_gpu = predict(nnet_gpu, imgs[0], local_img=True)
	prob_cpu = predict(nnet_cpu, imgs[0], local_img=True)

	print 'prob_gpu == prob_cpu {}'.format(prob_gpu==prob_cpu)
	print 'np.all(prob_gpu == prob_cpu) {}'.format(np.all(prob_gpu==prob_cpu))
	print 'np.any(prob_gpu == prob_cpu) {}'.format(np.any(prob_gpu==prob_cpu))

	for key in nnet_cpu.keys():
		print '\n Layer: {}'.format(key)
		try:
			gpuW = nnet_gpu[key].W.get_value()
			cpuW = nnet_cpu[key].W.get_value()
			print 'gpuW: {}'.format(gpuW)
			print 'cpuW: {}'.format(cpuW)
			print 'gpuW.shape == cpuW.shape : {}'.format(gpuW.shape==cpuW.shape )
			print 'np.all(gpuW == cpuW) : {}'.format(np.all(gpuW==cpuW))
			print 'np.any(gpuW == cpuW) : {}'.format(np.any(gpuW==cpuW))
		except:
			print 'problem with layer {}'.format(key)
