from abc import ABC, abstractmethod
import numpy as np
import importlib
import matplotlib.pyplot as plt
import tensorflow as tf
# import re

class Learner(ABC): 
    def __init__(self, stack_pointer, current_threshold, input_size, output_size):
        self.stack_pointer = stack_pointer
        self.current_threshold = current_threshold
        self.model = None
        self.input_size = input_size
        self.output_size = output_size

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def run(self, epochs, input_data, output_data):
        pass

    @abstractmethod
    def make_space(self, input_num):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def update_graphs(self, history, epoch_num):
        pass

    @abstractmethod
    def sweep(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    class LossHistory(tf.keras.callbacks.Callback):
        def on_train_begin(self, logs={}):
            self.losses = []
            self.val_losses = []

        def on_epoch_end(self, epoch, logs={}):
            self.losses.append(logs.get('loss'))
            self.val_losses.append(logs.get('val_loss'))