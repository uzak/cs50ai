"""Visualize filters from a model. Uses code from: 
https://machinelearningmastery.com/how-to-visualize-filters-and-feature-maps-in-convolutional-neural-networks/
"""

import sys
import tensorflow as tf
import cv2 as cv
from keras.models import Model
from matplotlib import pyplot

IMG_WIDTH = 30
IMG_HEIGHT = 30

# Ensure correct usage
if len(sys.argv) != 3:
    sys.exit("Usage: python match.py model.h5 filename")

model = tf.keras.models.load_model(sys.argv[1])

image_fn = sys.argv[2]
# Open image
img = cv.imread(image_fn)
img = cv.resize(img, (IMG_WIDTH, IMG_HEIGHT))


for i, layer in enumerate(model.layers):
	# check for convolutional layer
	if 'conv' not in layer.name:
		continue
	# get filter weights
	filters, biases = layer.get_weights()
	print(i, layer.name, filters.shape)

model = Model(inputs=model.inputs, outputs=model.layers[1].output)
feature_maps = model.predict(img.reshape(1, 30, 30, 3))
print(feature_maps.argmax())


# plot all 16 maps in an 4x4 squares
square = 4
ix = 1
for _ in range(square):
	for _ in range(square):
		# specify subplot and turn of axis
		ax = pyplot.subplot(square, square, ix)
		ax.set_xticks([])
		ax.set_yticks([])
		# plot filter channel in grayscale
		pyplot.imshow(feature_maps[0, :, :, ix-1], cmap='gray')
		ix += 1
# show the figure
pyplot.show()