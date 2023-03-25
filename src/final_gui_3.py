import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *

import numpy as np
import matplotlib.pyplot as plt
import tensorflow_prediction
import datetime
import Blackboard
import image_timestamp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from PIL import Image, ImageTk
import os,random

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1200x800")
        self.master.title("Input Form")

        # Define the dropdown menu options and their corresponding number of input fields
        self.options = {
            "Matlab_Sim_1": [("Input 1", 0), ("Input 2", 1)],
            "Matlab_Sim_2": [("Input 1", 0), ("Input 2", 1), ("Input 3", 2)],
            "Matlab_Sim_3": [("Input 1", 0), ("Input 2", 1), ("Input 3", 2), ("Input 4", 3)],
        }

        # Create the dropdown menu
        self.selected_option = tk.StringVar()
        self.selected_option.set(next(iter(self.options)))
        self.option_menu = tk.OptionMenu(self.master, self.selected_option, *self.options.keys(), command=self.show_input_fields)
        self.option_menu.pack()

        # Create the input fields and save button
        self.input_fields = []
        self.save_button = tk.Button(self.master, text="Send to Model", command=self.save_inputs)


        self.train_button = tk.Button(self.master, text="Train Model", command=self.call_blackboard)
        self.train_button.pack()


        #Display image of model training process
        # open the image file using PIL
        image_file = Image.open("image.png")
        resized_image = image_file.resize((250, 250))
        # convert the image to a PhotoImage object
        self.image = ImageTk.PhotoImage(resized_image)

        # create a label to display the image
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.pack(pady=10)


        #Create a Treeview Widget to display saved inputs and corresponding ML Blackboard output |Input|Model|Prediction|

        self.input_output_tree =  ttk.Treeview(column=("c1", "c2", "c3","c4","c5"), show='headings', height=10)
        self.input_output_tree.column("# 1", anchor=CENTER)
        self.input_output_tree.heading("# 1", text="INPUT")
        self.input_output_tree.column("# 2", anchor=CENTER)
        self.input_output_tree.heading("# 2", text="MODEL")
        self.input_output_tree.column("# 3", anchor=CENTER)
        self.input_output_tree.heading("# 3", text="PREDICTED")
        self.input_output_tree.column("# 4", anchor=CENTER)
        self.input_output_tree.heading("# 4", text="EXPECTED")
        self.input_output_tree.column("# 5", anchor=CENTER)
        self.input_output_tree.heading("# 5", text="ERROR")
        self.input_output_tree.pack(side='bottom',pady=25)

    def call_blackboard(self):
        Blackboard.main_loop()
        self.change_image() #Displayed image will update if new image is found
        print("TRAINING")

    def show_input_fields(self, *args):
        # Remove any existing input fields and the save button
        for input_field in self.input_fields:
            input_field[0].destroy()
            input_field[1].destroy()
        self.save_button.pack_forget()

        # Show the appropriate number of input fields based on the selected option
        fields_data = self.options[self.selected_option.get()]
        self.input_fields = [(tk.Label(self.master, text=title), tk.Entry(self.master)) for title, _ in fields_data]
        for i, (input_title, input_field) in enumerate(self.input_fields):
            input_title.pack()
            input_field.pack()
            _, field_type = fields_data[i]
            if field_type == 1:
                input_field.config(validate="key", validatecommand=(self.master.register(self.validate_float), '%P'))

        self.save_button.pack()

    def validate_float(self, value):
        if value.strip() == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def save_inputs(self):
        # Check that all inputs are valid integers or floats
        inputs = []
        for input_field in self.input_fields:
            input_title = input_field[0].cget("text")
            input_str = input_field[1].get()
            if not input_str:
                messagebox.showerror("Error", "Input fields cannot be empty")
                return
            try:
                input_num = float(input_str)
            except ValueError:
                messagebox.showerror("Error", f"{input_title} must be a valid integer or float")
                return
            inputs.append(input_num)



        # Append the inputs to the list and clear the input fields
        #self.inputs_list.append(inputs)
        self.inputs_list = (inputs)
        for input_field in self.input_fields:
            input_field[1].delete(0, tk.END)
        messagebox.showinfo("Success", "Inputs saved successfully!")

        #Display inputs, model, and output here
        self.display_inputs_outputs_tree()
    
    
    

    def change_image(self):
        # load the new image
        image_path = random.choice(os.listdir(os.path.join(os.getcwd(),'graphs')))
        new_image = Image.open(image_path) #THIS NEEDS TO BE DYNAMIC
        
        current_image_timestamp = image_timestamp.image_timestamp()
        print(last_image_timestamp)
        print(current_image_timestamp)
        
        if (last_image_timestamp!=current_image_timestamp):
            filepath = 'linear_fit.png'
            new_image = Image.open(filepath) #THIS NEEDS TO BE DYNAMIC
            # resize the new image
            resized_image = new_image.resize((250, 250))
            # update the PhotoImage object
            self.photo_image = ImageTk.PhotoImage(resized_image)
            # update the label with the new image
            self.image_label.config(image=self.photo_image)


    def call_tfpredict(self):
        model = 'Linear_Fit'
        predicted_output = tensorflow_prediction.predict([self.inputs_list])
        #output = 10 #CHANGE THIS HARDCORE TO TF.PREDICT()
        if (predicted_output != None):
            print("Sending inputs:",self.inputs_list)

            return model, predicted_output
        else:
            return None
        #Should return: model type, output

    def display_inputs_outputs_tree(self):
        ML_Model,ML_Prediction= self.call_tfpredict() ##CALL TF.PREDICT HERE
        real_value = self.inputs_list[0]*3+self.inputs_list[1]*2+self.inputs_list[2]*5+self.inputs_list[3]
        error = abs(real_value-ML_Prediction)/real_value
        error = (str(error))[2:-2]
        #only change update image and update tree if there are new values
        if ML_Model != None:
            #Create a 2x2 Treeview |Best Performing Model|Accuracy| ~= |'CNN'|0.81|
            self.input_output_tree.insert('', 'end', text=input, values=(str(self.inputs_list), ML_Model,(str(ML_Prediction))[2:-2],real_value,error))

    def show_input_fields(self, *args):
        # Remove any existing input fields and the save button
        for input_field in self.input_fields:
            input_field[0].destroy()
            input_field[1].destroy()
        self.save_button.pack_forget()

        # Show the appropriate number of input fields based on the selected option
        fields_data = self.options[self.selected_option.get()]
        self.input_fields = [(tk.Label(self.master, text=title), tk.Entry(self.master)) for title, _ in fields_data]
        for i, (input_title, input_field) in enumerate(self.input_fields):
            input_title.pack()
            input_field.pack()
            _, field_type = fields_data[i]
            if field_type == 1:
                input_field.config(validate="key", validatecommand=(self.master.register(self.validate_float), '%P'))

        self.save_button.pack()



if __name__ == "__main__":
    global last_image_timestamp
    root = tk.Tk()
    app = App(master=root)
    app.inputs_list = []
    last_image_timestamp = image_timestamp.image_timestamp()
    app.pack()
    root.mainloop()

