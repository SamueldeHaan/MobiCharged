import tensorflow as tf
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import gc
import learner_template

class LinearFit(learner_template.LearnerTemplate):

    def get_model(self):
        return self.model
    
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

    def set_minimum_threshold(self):
        if not(self.current_threshold):
            self.current_threshold = self.input_size

    def increase_threshold(self):
        self.current_threshold = min(self.current_threshold + 1, 10000)

    ##maybe this can be standardized across instances?
    def update_graphs(self, epoch_num):
        textstr = 'Training error=%.2f\nValidation error=%.2f\n'%(self.history.losses[-1], self.history.val_losses[-1])
        plt.plot(self.history.losses)
        plt.plot(self.history.val_losses)
        plt.title('Model Loss Over ' + str(epoch_num) + ' Epochs With Early Stopping')
        plt.text(0.02, 0.5, textstr, fontsize=14, transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.4)
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper right')
        #plt.savefig( os.path.basename(__file__).split('.')[0] + '.png')
        image_name = (os.path.basename(__file__).split('.')[0] + '.png')
        plt.savefig(os.path.join('src', 'matlab_images',image_name),overwrite = True)
        plt.close()

    ##need this to just empty the model and its weights instead and the Losshistory instead
    def sweep(self):
        del self
        gc.collect()

    def predict(self, new_X):
        new_X = np.array([new_X])
        predictions = self.model.predict(new_X)
        return predictions
    
    
# x = np.array([[1,2,3,4], [2,3,4,5], [3,4,5,6]]).astype(np.float32, copy=False)
# y = np.array([[1], [2] , [3]]).astype(np.float32, copy=False)
# l = LinearFit(0,0,1,2,3)
# l.setup()
# l.run(3, x , y)
# print(l.history)
# l.reset_history()
# print(l.history)
