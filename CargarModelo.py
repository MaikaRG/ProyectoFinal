from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import os
import tensorflow as tf
# load json and create model
def modelo():
    json_file = open('modelMasEntrenao.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("modelMasEntrenao.h5")
    print("Loaded model from disk")
    return loaded_model
