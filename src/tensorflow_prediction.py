import tensorflow as tf

import os
import numpy as np
import pandas as pd
from tensorflow import keras


# Load the saved model from the .h5 file
#model = tf.saved_model.load('current_best\model\saved_model.pb')

def custom_loss(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))


def predict(data):
    def custom_loss(y_true, y_pred):
        return tf.reduce_mean(tf.square(y_true - y_pred))

    print(data)
    model = keras.models.load_model('current_best\model', custom_objects={'custom_loss': custom_loss})
    # Make a prediction on a new data point
    #new_data = [[1.2, 1.5, 1.8, 1.9]]
    prediction = model.predict(data)
    #print(np.argmax(prediction))
    #print(prediction)
    return prediction