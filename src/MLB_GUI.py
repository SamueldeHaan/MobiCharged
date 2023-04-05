import threading
from tkinter import messagebox
import tkinter as tk
from tkinter import *
from tkinter import ttk

import queue_module
import tensorflow_prediction
import Blackboard
import os
from PIL import Image, ImageTk

import firestore as fs
import matlab_calculate


#GUI functionality:
# 1. Displays the ML blackboard's performance
# 2. Allows user to input parameters to test current best performing model's prediction
# 3. Display live training graph


class MyGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x900")
        self.master.title("Input Form")

        self.train_count = 0

        # Define the dropdown menu options and their corresponding number of input fields
        self.options = {
            #"Matlab_Sim_3": [("Input 1", 0), ("Input 2", 1)],
            #"Matlab_Sim_2": [("Input 1", 0), ("Input 2", 1), ("Input 3", 2)],
            "unknown_poly_type": [("Input 1", 0), ("Input 2", 1), ("Input 3", 2), ("Input 4", 3)],
        }

        # Create the dropdown menu
        self.selected_option = tk.StringVar()
        self.selected_option.set(next(iter(self.options)))
        self.option_menu = tk.OptionMenu(self.master, self.selected_option, *self.options.keys(), command=self.show_input_fields)
        self.option_menu.pack()

        # Create the input fields and save button, save_button is .packed() in show_input_fields(); user must select an option first
        self.input_fields = []
        self.save_button = tk.Button(self.master, text="Send to Model", command=self.save_inputs)
        

        #Button to send inputs to model
        self.train_button = tk.Button(self.master, text = "ML Blackboard start", command = self.train_thread)
        self.train_button.pack()


        #Create a Treeview Widget to display saved inputs and corresponding ML Blackboard output |Input|Model|Prediction|
        self.tree_frame = tk.Frame(master)
        self.tree_frame.pack(fill='both')
        self.input_output_tree =  ttk.Treeview(self.tree_frame,column=("c1", "c2", "c3","c4","c5"), show='headings', height=5)
        self.input_output_tree.column("# 1", anchor=CENTER)
        self.input_output_tree.heading("# 1", text="INPUT")
        self.input_output_tree.column("# 2", anchor=CENTER)
        self.input_output_tree.heading("# 2", text="MODEL TYPE")
        self.input_output_tree.column("# 3", anchor=CENTER)
        self.input_output_tree.heading("# 3", text="OUTPUT")
        self.input_output_tree.column("# 4", anchor=CENTER)
        self.input_output_tree.heading("# 4", text="EXPECTED OUTPUT")
        self.input_output_tree.column("# 5", anchor=CENTER)
        self.input_output_tree.heading("# 5", text="ERROR")


        yscrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.input_output_tree.yview)
        self.input_output_tree.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side='right', fill='y')
        self.input_output_tree.pack(fill='both',expand=True,side='bottom',pady=25)

        #Display how many times training has been completed

        self.train_label = tk.Label(master, text = "Number of Training Iterations= {}".format(str(self.train_count)))
        self.train_label.pack()

        #Display training history
        self.train_tree_frame = tk.Frame(master)
        self.train_tree_frame.pack(fill='both')
        self.train_tree =  ttk.Treeview(self.tree_frame,column=("c1", "c2", "c3","c4"), show='headings', height=5)
        self.train_tree.column("# 1", anchor=CENTER)
        self.train_tree.heading("# 1", text="Iteration #")
        self.train_tree.column("# 2", anchor=CENTER)
        self.train_tree.heading("# 2", text="MODEL TYPE")
        self.train_tree.column("# 3", anchor=CENTER)
        self.train_tree.heading("# 3", text="ERROR")
        self.train_tree.column("# 4", anchor=CENTER)
        self.train_tree.heading("# 4", text="# Datapoints Available At Start")

        yscrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.train_tree.yview)
        self.train_tree.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side='right', fill='y')
        self.train_tree.pack(fill='both',expand=True,side='bottom',pady=25)

        #Display image of model training process
        self.image_label = tk.Label(master , text = "Current Best Model:")
        self.image_label.pack()


        # start a timer to update the image periodically
        self.update_image()


    def update_image(self):
        #Routinely check if the image name is inserted into queue (done in blackboard.py)
        #If a file_name is inserted, then try opening the image from matlab_images folder
        try:
            model_name = str(queue_module.my_queue.get(timeout=0.1))
            print(model_name)
            if model_name is not None: 
                #additional bug-prevention = check for type of variable, or if file name belongs to list of possible model types
                
                print("MODEL NAME IS NOT NONE, UPDATE IMAGE:",model_name)
                filepath = os.path.join(os.getcwd(),'matlab_images',model_name+'.png')
                new_image = Image.open(filepath) #THIS NEEDS TO BE DYNAMIC
                resized_image = new_image.resize((250,250))
                #Open the PIL image as an ImageTk.PhotoImage object to be inserted into Tkinter widget
                tk_image = ImageTk.PhotoImage(resized_image)

            # update the PhotoImage object in the label
                #note: compound takes second parameter (image) and places it 'bottom' relative to first parameter (text)
                self.image_label.configure(text = "Current Best Model: {}".format(model_name),image = tk_image,compound = "bottom")
                self.image_label.image = tk_image
        except Exception:
            pass
        self.master.after(1000, self.update_image)


    def validate_float(self, value):
        if value.strip() == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    #Function that shows the input fields for each option in dropdown menu
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
        
        

    #Input fields then send to tf.model.predict
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
        #Display inputs, model, and output here
        try:
            self.display_inputs_outputs_tree()
        except:
            pass
    
    def display_inputs_outputs_tree(self):
        ML_Model,ML_Prediction = self.call_tfpredict() ##CALL TF.PREDICT HERE
        matlab_sim_filename = self.selected_option.get() #this is from the dropdown menu, value = currently selected matlab simulation file
        matlab_output = matlab_calculate.calculate(str(matlab_sim_filename),self.inputs_list)
        if matlab_output == Exception:
            matlab_output = 'N/A'
            messagebox.showinfo("Error","{}.m cannot be found in src/matlab".format(str(matlab_sim_filename)))
            error = 'N/A'
        else:
            error = '% {:.2f}'.format(100*abs(float(ML_Prediction)-matlab_output)/matlab_output)

        print (matlab_output,error)
        #only change update image and update tree if there are new values
        if ML_Model != None:
            self.input_output_tree.insert('', 'end', text=input, values=(str(self.inputs_list), ML_Model,ML_Prediction,matlab_output,error))

    #This function passes user input to tf.model.predict()
    def call_tfpredict(self):
        model_name = self.get_model_name()
        if model_name != None:
            output = tensorflow_prediction.predict([(self.inputs_list)])
            if (output != None): #just in case model folder gets deleted, but best.txt exists.
                print("Sending inputs:",self.inputs_list)
                #output returns as double list [[__]], remove outer brackets
                output = str(output)[2:-2]
                messagebox.showinfo("Success", "Inputs saved successfully!")
                return model_name ,output
            else:
                messagebox.showerror("Error 0","Error, there is no file named 'best.txt' or it is empty, Please press start first.")
                return None, None, None

        else:
            messagebox.showerror("Error 1","Error, there is no trained model to test on. Please press start first.")
            

    def get_model_name(self):
        try:
            with open(os.path.join(os.getcwd(),'current_best','best.txt'),'r') as f:
                model_name = str(f.readlines()[0])
                return model_name
        except:
            return None
    def get_model_current_error(self):
        try:
            with open(os.path.join(os.getcwd(),'current_best','current_error.txt'),'r') as f:
                current_error = str(f.readlines()[0])
                return current_error
        except:
            return None



    #should add try except for debug
    def train_thread(self):
        current_dataset_size = fs.check_count() # we want count before we start training
        mlb_thread = threading.Thread(target = Blackboard.run)
        mlb_thread.start()
        mlb_thread.join()
        self.train_count += 1
        self.train_label.config(text="Number of Training Iterations= {}".format(str(self.train_count)))
        model_name = self.get_model_name()
        current_error = self.get_model_current_error()

        if model_name != None and current_error != None:
            self.train_tree.insert('','end',text = input, values = (self.train_count,model_name,current_error,str(current_dataset_size)) )

def main():
    root = tk.Tk()
    gui = MyGUI(root)
    root.mainloop()
    
if __name__ == '__main__':
    MyGUI.inputs_list = []
    main()