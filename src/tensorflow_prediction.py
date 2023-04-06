#### This script will be called by user when they input values
#Returns prediction output of best tf model

import tensorflow as tf

import os
from tensorflow import keras


# Load the saved model from the .h5 file
#model = tf.saved_model.load('current_best\model\saved_model.pb')

def custom_loss(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))


def predict(data):
    def custom_loss(y_true, y_pred):
        return tf.reduce_mean(tf.square(y_true - y_pred))

    print(data)
    path = (os.path.join(os.getcwd(),'current_best','model'))
    print(path)
    try:
        model = keras.models.load_model((os.path.join(os.getcwd(),'current_best','model')), custom_objects={'custom_loss': custom_loss})
        prediction = model.predict(data)
        return prediction
    except:
        pass

    # Make a prediction on a new data point
    #new_data = [[1.2, 1.5, 1.8, 1.9]]
    
    #print(np.argmax(prediction))
    #print(prediction)
    

#x = predict([[1,2,3,4]])
#print(x)