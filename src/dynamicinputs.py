import tkinter as tk

class InputFieldsGUI:
    def __init__(self, master):
        self.master = master
        self.options = ["Option 1", "Option 2", "Option 3"]
        self.num_inputs = {"Option 1": 3, "Option 2": 2, "Option 3": 1}
        self.input_fields = []
        
        self.option_var = tk.StringVar()
        self.option_var.set(self.options[0])
        
        self.generate_button = tk.Button(self.master, text="Generate Inputs", command=self.generate_inputs)
        self.generate_button.pack()
        
        self.print_button = tk.Button(self.master, text="Print Inputs", command=self.print_inputs, state=tk.DISABLED)
        self.print_button.pack()
    
    def generate_inputs(self):
        option = self.option_var.get()
        num_fields = self.num_inputs[option]
        
        # clear any existing input fields
        for field in self.input_fields:
            field.destroy()
        self.input_fields = []
        
        # create the input fields for the selected option
        for i in range(num_fields):
            label = tk.Label(self.master, text="Input {}".format(i+1))
            label.pack()
            entry = tk.Entry(self.master)
            entry.pack()
            self.input_fields.append(entry)
        
        # enable the print button
        self.print_button.config(state=tk.NORMAL)
    
    def print_inputs(self):
        # retrieve the user's inputs from the input fields
        inputs = [entry.get() for entry in self.input_fields]
        
        # print the user's inputs
        print("User inputs:")
        for i, val in enumerate(inputs):
            print("Input {}: {}".format(i+1, val))
        
root = tk.Tk()
gui = InputFieldsGUI(root)
root.mainloop()
