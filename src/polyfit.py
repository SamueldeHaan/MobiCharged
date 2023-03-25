import tensorflow as tf
import numpy as np
import threading as th

# In the future, this file and other files like it will implement a standard Model Interface
# Define the input and output matrices
X = np.random.rand(100, 4)
s = th.Semaphore(1)
input_size = 4
Y = 3 * X[:,0] ** 2 + 2 * X[:,1] + 5*X[:,2] + 6*X[:,3] +  1 + np.random.normal(0, 0.1, 100)

#############Might wanna put all this in a separate higher level file
# Define the model

class LossHistory(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
        self.val_losses = []

    def on_epoch_end(self, epoch, logs={}):
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))

def setup():
    try:
        global model 
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(1, input_shape=(input_size,), kernel_regularizer=tf.keras.regularizers.l2(0.01)))

        # Compile the model with a custom loss function - Least squares
        def custom_loss(y_true, y_pred):
            return tf.reduce_mean(tf.square(y_true - y_pred))

        #Gradient Descent right now
        optimizer = tf.keras.optimizers.SGD(learning_rate=0.1)
        model.compile(optimizer=optimizer, loss=custom_loss)
        return True
    except Exception as e:
        print("Error:" + str(e))
        return False

def run(epoch_num, input_data, output_data):
    s.acquire()
    history = LossHistory()
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    model.fit(input_data, output_data, epochs=epoch_num, validation_split=0.2, callbacks=[history, early_stopping])
    s.release()
    return history

def pred(new_X):
    # Make predictions with the trained model - currently only one at a time
    s.acquire()
    new_X = np.array([new_X])
    predictions = model.predict(new_X)
    s.release()
    return predictions 


# setup()
# run(100, X, Y)
# setup()
# try:
#     run(100, np.array([ [10.0123, 20.0, 11.055, 21.0], [1.0, 2.0, 3.044353453345, 4.0], [5.0, 6.02222222, 7.0, 8.0] ]).astype(float, copy=False), np.array([27.0, 32.0, 45.0]).astype(float, copy=False))
# except Exception as e:
#     print(e)


# print("PREDICTION:" + str(pred([1,2,3])))

##-----------------------------

##will be added later - will test on both normalized and non-normalized and compare
##def normalize():
##    return

def old_params(): ##for retraining?
    return