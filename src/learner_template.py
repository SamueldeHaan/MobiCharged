from abc import ABC, abstractmethod
import tensorflow as tf
# import re

class LearnerTemplate(ABC): 
    def __init__(self, stack_pointer, current_threshold, performance_count, input_size, output_size):
        self.stack_pointer = stack_pointer
        self.current_threshold = current_threshold
        self.performance_count = performance_count
        self.model = None
        self.input_size = input_size
        self.output_size = output_size
        self.history = self.LossHistory()
        # self.minimum_data = None
        self.set_minimum_threshold()

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def run(self, epochs, input_data, output_data):
        pass

    # don't think we need this -> local copy of table entries will be stored in matrix by Blackboard
    # @abstractmethod
    # def make_space(self, input_num):
    #     pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def set_minimum_threshold(self):
        pass

    @abstractmethod
    def increase_threshold(self):
        pass

    @abstractmethod
    def update_graphs(self, history, epoch_num):
        pass

    @abstractmethod
    def sweep(self):
        pass

    @abstractmethod
    def predict(self, new_X):
        pass

    # def reset_history(self):
    #     self.history = self.LossHistory()

    class LossHistory(tf.keras.callbacks.Callback):
        def on_train_begin(self, logs={}):
            self.losses = []
            self.val_losses = []

        def on_epoch_end(self, epoch, logs={}):
            self.losses.append(logs.get('loss'))
            self.val_losses.append(logs.get('val_loss'))