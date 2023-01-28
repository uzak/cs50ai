import sys
import tensorflow as tf
import cv2 as cv


IMG_WIDTH = 30
IMG_HEIGHT = 30

# Ensure correct usage
if len(sys.argv) != 3:
    sys.exit("Usage: python match.py model.h5 filename")

model = tf.keras.models.load_model(sys.argv[1])

image_fn = sys.argv[2]
# Open image
img = cv.imread(image_fn)
res = cv.resize(img, (IMG_WIDTH, IMG_HEIGHT))

print(model.predict( res.reshape(1, 30, 30, 3)).argmax())
#model.predict(res)

