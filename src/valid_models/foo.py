

import learner_template
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import gc

class Poop(learner_template.LearnerTemplate):
    
    def run(self, epoch_num, input_data, output_data):
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
        self.model.fit(input_data, output_data, epochs=epoch_num, validation_split=0.2, callbacks=[self.history, early_stopping])

    def setup(self):
        try: 
            self.model = tf.keras.Sequential()
            self.model.add(tf.keras.layers.Dense(1, input_shape=(self.input_size,), kernel_regularizer=tf.keras.regularizers.l2(0.01)))

            #Least squares
            def custom_loss(y_true, y_pred):
                return tf.reduce_mean(tf.square(y_true - y_pred))

            #Gradient Descent
            optimizer = tf.keras.optimizers.SGD(learning_rate=0.1)
            self.model.compile(optimizer=optimizer, loss=custom_loss)
            return True
        except Exception as e:
            print("Error:" + str(e))
            return False

    ##maybe this can be standardized across instances?
    def update_graphs(self, history, epoch_num):
        textstr = 'Training error=%.2f\nValidation error=%.2f\n'%(history.losses[-1], history.val_losses[-1])
        plt.plot(history.losses)
        plt.plot(history.val_losses)
        plt.title('Model Loss Over ' + str(epoch_num) + ' Epochs With Early Stopping')
        plt.text(0.02, 0.5, textstr, fontsize=14, transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.4)
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper right')
        plt.savefig( os.path.basename(__file__).split('.')[0] + '.png')
        plt.close()

    def sweep(self):
        del self
        gc.collect()
