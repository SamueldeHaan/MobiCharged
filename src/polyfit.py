import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


# Define the input and output matrices
X = np.random.rand(100, 3)

Y = 3 * X[:,0] ** 2 + 2 * X[:,1] + 1 + np.random.normal(0, 0.1, 100)

#############Might wanna put all this in a separate higher level file
# Define the model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(1, input_shape=(3,), kernel_regularizer=tf.keras.regularizers.l2(0.01)))

# Compile the model with a custom loss function
def custom_loss(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))

optimizer = tf.keras.optimizers.SGD(learning_rate=0.1)
model.compile(optimizer=optimizer, loss=custom_loss)

class LossHistory(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_epoch_end(self, epoch, logs={}):
        self.losses.append(logs.get('loss'))


history = LossHistory()
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

model.fit(X, Y, epochs=100, validation_split=0.2, callbacks=[history, early_stopping])

plt.plot(range(1,101), history.losses)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()
#------------------------------------


# Fit the model to the data
model.fit(X, Y, epochs=100)

def pred():
    # Make predictions with the trained model
    new_X = np.random.rand(10, 3)
    predictions = model.predict(new_X)
    return predictions 

##will be added later - will test on both normalized and non-normalized and compare
##def normalize():
##    return

def old_params(): ##for retraining?
    return