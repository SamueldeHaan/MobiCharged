import tkinter as tk
import tkinter.filedialog
import os.path
from tkinter import messagebox
import server_initializer
import simulation_check

"""
Author: Mustafa Choueib
Last Revision Date: March 23rd, 2023.
Purpose: The purpose of this is to create a simple user interface for a more appealing way of interacting and configuring the MobiCharged application.
"""



global numInputs, numOutputs, simTestPassed, inputRanges
numInputs = 0
numOutputs = 0
simTestPassed = False
inputRanges = []

root = tk.Tk()
root.title("MobiCharged Initializer")
root.configure(bg="#222222")

#Creating Title with an image
image_label = tk.Label(root, borderwidth=2, relief="groove")
image_label.pack(expand=True, pady=(50,0))
image = tk.PhotoImage(file="mobicharged.png")
image_label.config(image=image)
title_label = tk.Label(root, text="MobiCharged Initializer", font=("Arial", 24), fg="blue")
title_label.pack()


# create a frame for the integer input fields
int_frame = tk.Frame(root, bg="#222222")
int_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=(50,0))

#Frame for new fields
add_frame = tk.Frame(root, bg="#222222")
add_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

def validate_int(value):
    if value == "":
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False

# create the two integer input fields
int_label_1 = tk.Label(int_frame, text="Enter the Number of Inputs Expected:", fg="#ffffff", bg="#222222")
int_label_1.pack(side=tk.LEFT, padx=(0, 10))
int_entry_1 = tk.Entry(int_frame, width=10)
int_entry_1.pack(side=tk.LEFT, padx=(0, 20))
int_entry_1.config(validate="key", validatecommand=(int_entry_1.register(validate_int), "%P"))
int_label_2 = tk.Label(int_frame, text="Enter the Number of Outputs Expected:", fg="#ffffff", bg="#222222")
int_label_2.pack(side=tk.LEFT, padx=(0, 10))
int_entry_2 = tk.Entry(int_frame, width=10)
int_entry_2.pack(side=tk.LEFT, padx=(0, 20))
int_entry_2.config(validate="key", validatecommand=(int_entry_2.register(validate_int), "%P"))

# function to show additional input fields when int_entry_1 is filled out
def show_additional_fields(event):
    try:
        #numOutputs = int(int_entry_2.get())
        num_additional_fields = int(int_entry_1.get())
        
        #Destroys existing additional fields if value is changed
        for widget in add_frame.winfo_children():
            if widget.winfo_class() == "Entry" or widget.winfo_class() == "Label":
                widget.destroy()
        for i in range(num_additional_fields):
            # create a label and entry for each additional field
            add_label = tk.Label(add_frame, text=f"Min Input #{i+1}:", fg="#ffffff", bg="#222222")
            add_label.pack(side=tk.LEFT, padx=(0, 10))
            add_entry = tk.Entry(add_frame, width=10)
            add_entry.pack(side=tk.LEFT, padx=(0, 20))
            # validate the entry to ensure it's a float or integer
            add_entry.config(validate="key", validatecommand=(add_entry.register(validate_float_or_int), "%P"))
            # create a label and entry for each additional field
            add_label = tk.Label(add_frame, text=f"Max Input#{i+1}:", fg="#ffffff", bg="#222222")
            add_label.pack(side=tk.LEFT, padx=(0, 10))
            add_entry = tk.Entry(add_frame, width=10)
            add_entry.pack(side=tk.LEFT, padx=(0, 20))
            # validate the entry to ensure it's a float or integer
            add_entry.config(validate="key", validatecommand=(add_entry.register(validate_float_or_int), "%P"))
    except ValueError:
        pass

# bind show_additional_fields to the <FocusOut> event of int_entry_1
int_entry_1.bind("<FocusOut>", show_additional_fields)



# function to validate a string as a float or integer
def validate_float_or_int(new_value):
    if new_value == "":
        return True
    try:
        float(new_value)
        return True
    except ValueError:
        return False


# function to open a file explorer and display the selected file path
def open_file_explorer():
    global simTestPassed
    filename = tk.filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)
    simTestPassed = False


#Calls server_initializer to check the selected simulation file with the desired configuration
def test_matlab_sim():
    global numOutputs, numInputs, simTestPassed
    if(len(file_entry.get()) == 0):
        messagebox.showerror("Error", "Please select a MATLAB simulation file") 
        return False
    
    elif(len(int_entry_1.get()) == 0 or int(int_entry_1.get()) <= 0):
        messagebox.showerror("Error", "Please enter the number of expected Inputs (positive value)")
        return False
    elif(len(int_entry_2.get()) == 0 or int(int_entry_2.get()) <= 0):
        messagebox.showerror("Error", "Please enter the number of expected Outputs (positive value)")
        return False

    numInputs = int_entry_1.get()
    numOutputs = int_entry_2.get()

    PathToSimFile = file_entry.get()    
    SimTest = simulation_check.CheckMatlabSimulation(PathToSimFile, numInputs, numOutputs)
    
    #SimTest = True is required to launch the server, thus, user must test a selected MATLAB file
    if(SimTest):
        messagebox.showinfo("Success", "Simulation file passed the check with the specified parameters!")
        simTestPassed = True
    else:
        messagebox.showerror("Error", "Simulation file did not pass the check with the specified parameters, input new parameters or select a different simulation file!")
        simTestPassed = False

#Launches the server once all the conditions have been met
def start_mobicharged_server():
    global numInputs, numOutputs, simTestPassed, inputRanges
    if(len(int_entry_1.get()) == 0 or int(int_entry_1.get()) <= 0):
        messagebox.showerror("Error", "Please enter the number of expected Inputs (positive value)")
        return False
    elif(len(int_entry_2.get()) == 0 or int(int_entry_2.get()) <= 0):
        messagebox.showerror("Error", "Please enter the number of expected Outputs (positive value)")
        return False
    elif(not check_min_max_ranges()):
        messagebox.showerror("Error", "There is a missing value for one of the ranges!")
        return False
    elif(not simTestPassed or not validate_file_exists(file_entry.get())):
        messagebox.showerror("Error", "The currently selected MATLAB simulation file has not passed the simulation check or does not exist!")
        return False
    
    counter = 0
    newWidgetList = []
    for widget in add_frame.winfo_children():
        if widget.winfo_class() == "Entry":
            newWidgetList.append(widget.get())
    
    for i in range(int(numInputs)):
        tempList = []
        tempList.append(newWidgetList[counter])
        tempList.append(newWidgetList[counter+1])
        inputRanges.append(tempList)
        counter += 2
    try:
        fileName = file_entry.get()
        server_initializer.createLaunchBat(numInputs, numOutputs, inputRanges, fileName)
    except:
        messagebox.showerror("Error", "Could not start the server! Try again later.")
        return False
#Ensures that all the ranges are entered correctly
def check_min_max_ranges():
    allRangesGood = True
    for widget in add_frame.winfo_children():
        if widget.winfo_class() == "Entry":
            if(len(widget.get()) == 0):
                allRangesGood = False
    return allRangesGood  

# create a frame for the file explorer and file input field
file_frame = tk.Frame(root, bg="#222222")
file_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=(0,50))

# create the file input field and button to open the file explorer
file_label = tk.Label(file_frame, text="Select a  Simulation file:", fg="#ffffff", bg="#222222")
file_label.pack(side=tk.LEFT, padx=(0, 10))
file_entry = tk.Entry(file_frame, width=30)
file_entry.pack(side=tk.LEFT, padx=(0, 20))
file_button = tk.Button(file_frame, text="Browse", command=open_file_explorer)
file_button.pack(side=tk.LEFT)
Simfile_button = tk.Button(file_frame, text="Test Simulation File", command=test_matlab_sim)
Simfile_button.pack(side=tk.LEFT)

start_server_button = tk.Button(file_frame, text="Launch MobiCharged Server", command=start_mobicharged_server)
start_server_button.pack(side=tk.RIGHT, expand=True, padx=(20,0))

# function to validate that a file exists
def validate_file_exists(filename):
    if os.path.isfile(filename):       
        return True
    else:
        messagebox.showerror("Error", f"File '{filename}' does not exist")
        return False



# validate the file input field to ensure the file exists
file_entry.config(validate="none", validatecommand=(file_entry.register(validate_file_exists), "%P"))



root.mainloop()