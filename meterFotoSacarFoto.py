from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.transform import resize
import numpy as np
from keras.applications.inception_resnet_v2 import preprocess_input
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from skimage.io import imsave
import CargarModelo
import tensorflow as tf
import os
import webbrowser

def create_inception_embedding(grayscaled_rgb):
    inception = InceptionResNetV2(weights='imagenet', include_top=True)
    #inception.graph = tf.compat.v1.get_default_graph()
    grayscaled_rgb_resized = []
    for i in grayscaled_rgb:
        i = resize(i, (299, 299, 3), mode='constant')
        grayscaled_rgb_resized.append(i)
    grayscaled_rgb_resized = np.array(grayscaled_rgb_resized)
    grayscaled_rgb_resized = preprocess_input(grayscaled_rgb_resized)
    embed = inception.predict(grayscaled_rgb_resized)
    return embed

def resizePutasImagenes(path):
  color_me = (img_to_array(load_img(path)))
  color_me =resize(color_me, (256, 256), mode='constant')
  imsave(path, color_me)

def resizeImages(path):
    resizePutasImagenes(path)
    color_me = []
    for filename in os.listdir('./input/'):
      color_me.append(img_to_array(load_img('./input/'+filename)))
    color_me = np.array(color_me, dtype=float)
    gray_me = gray2rgb(rgb2gray(1.0/255*color_me))
    color_me_embed = create_inception_embedding(gray_me)
    color_me = rgb2lab(1.0/255*color_me)[:,:,:,0]
    color_me = color_me.reshape(color_me.shape+(1,))
    output=CargarModelo.modelo().predict([color_me, color_me_embed])
    output = output*128
    for i in range(len(output)):
      cur = np.zeros((256, 256, 3))
      cur[:,:,0] = color_me[i][:,:,0]
      cur[:,:,1:] = output[i]
      imsave('./output/img.png', lab2rgb(cur))
    #return webbrowser.open('./output/img.png')
#resizeImages()