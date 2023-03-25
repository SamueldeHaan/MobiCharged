import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import threading as th
import concurrency_monitor

monitor = None

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x800")
        self.master.title("Input Form")

        # Define the dropdown menu options and their corresponding number of input fields
        self.options = {
            "Option 1": [("Input 1", 0), ("Input 2", 1)],
            "Option 2": [("Input 1", 0), ("Input 2", 1), ("Input 3", 2)],
            "Option 3": [("Input 1", 0), ("Input 2", 1), ("Input 3", 2), ("Input 4", 3)],
            "Option 4": [("Input 1", 0), ("Input 2", 1), ("Input 3", 2), ("Input 4", 3), ("Input 5", 4)]
        }

        # Create the dropdown menu
        self.selected_option = tk.StringVar()
        self.selected_option.set(next(iter(self.options)))
        self.option_menu = tk.OptionMenu(self.master, self.selected_option, *self.options.keys(), command=self.show_input_fields)
        self.option_menu.pack()

        # Create the input fields and save button
        self.input_fields = []
        self.save_button = tk.Button(self.master, text="Send to Model", command=self.save_inputs)

         # create a matplotlib figure and canvas to display the graph
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack()

        # create an initial plot, ideally we fetch these values from ML blackboard and just update
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x)
        self.plot = self.figure.add_subplot(111)
        self.plot.plot(x, y)

        #MATPLOTLIB UPDATE FUNCTION HERE
        # def update_value(self):
        #     # get the new value from the entry widget
        # new_value = int(self.value_entry.get())
        
        # # update the value label
        # self.value = new_value
        # self.value_label.config(text="Current value: {}".format(self.value))

        # # update the plot with the new value
        # x = np.linspace(0, 2*np.pi, 100)
        # y = np.sin(x + self.value)
        # self.plot.clear()
        # self.plot.plot(x, y)
        # self.canvas.draw()


        #this is a function that updates the value fo the matplotlib




        #Create a Treeview Widget to display saved inputs and corresponding ML Blackboard output |Input|Model|Prediction|

        self.input_output_tree =  ttk.Treeview(column=("c1", "c2", "c3"), show='headings', height=5)
        self.input_output_tree.column("# 1", anchor=CENTER)
        self.input_output_tree.heading("# 1", text="INPUT")
        self.input_output_tree.column("# 2", anchor=CENTER)
        self.input_output_tree.heading("# 2", text="MODEL")
        self.input_output_tree.column("# 3", anchor=CENTER)
        self.input_output_tree.heading("# 3", text="OUTPUT")

        self.input_output_tree.pack()




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
        self.inputs_list.append(inputs)
        for input_field in self.input_fields:
            input_field[1].delete(0, tk.END)
        messagebox.showinfo("Success", "Inputs saved successfully!")

        #Display inputs, model, and output here
        self.display_inputs_outputs_tree()
        
    def call_tfpredict(inputs):
        print("Sending inputs:",inputs)
        #async function


        return 'Linear',3.02
        #Should return: model type, output


   #---------------
    def worker_thread(request, response, monitor, in_event, out_event):
        # retrieve the shared data object from the queue
        while True:
            in_event.wait()
            in_event.unset()
            #expecting [val,val,val,val]
            value = monitor.get_payload()
            response = (value[0], value[1].predict(request))
            out_event.set()

    global in_event, out_event, request, response
    in_event = th.Event()
    out_event = th.Event()
    request = None
    response = None
    # create worker thread
    thread = th.Thread(target=worker_thread, args=(request, response, monitor, in_event, out_event))
    thread.start()
    #---------------

    def display_inputs_outputs_tree(self):
        global in_event, out_event, request, response
        request = self.inputs_list

        in_event.set()
        out_event.wait()
        out_event.unset()

        #for i, input in enumerate(self.inputs_list):
        self.input_output_tree.insert('', 'end', text=input, values=(self.inputs_list, response[0], response[1]))

 
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

def run(m):
    global monitor
    monitor = m
    root = tk.Tk()
    app = App(master=root)
    app.inputs_list = []
    app.pack()
    root.mainloop()

