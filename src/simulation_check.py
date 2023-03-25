import matlab.engine
import os



'''
Author: Mustafa Choueib
Last Revision Date: March 23rd, 2023.
Purpose: This script runs a check on matlab simulation files to ensure they are compatible with the desired input configurations specified by the user.
'''


#Runs a quick check with the MATLAB simulation file and given input/output parameters specified in the GUI and ensures it is compatible.
def CheckMatlabSimulation(SimulationPath, numInputs, numOutputs):
    numInputs = int(numInputs)
    numOutputs = int(numOutputs)
    #Initializing MATLAB engine with the specified file path
    try:
        eng = matlab.engine.start_matlab()
        path = eng.genpath(SimulationPath)
        eng.addpath(path, nargout=0)
    except Exception as e:
        print(e)
        return validSimFile
    
    #Extracting just the filename from the specified path
    fileName = os.path.basename(SimulationPath)
    fileName = os.path.splitext(fileName)[0]
    #functionString creates a string function call to matlab engine and is then evaluated.
    functionString = "eng." + fileName + "("

    #Appending the number of inputs specified to the function call
    for i in range(numInputs):
        functionString = functionString + str(i) + ","

    functionString = functionString + "nargout=1)"
    
    #Testing the MATLAB simulation file with the specified inputs, true if it passes, false otherwise.
    try:
        y = eval(functionString)
        validSimFile = True
        return validSimFile
    except Exception as e:
        validSimFile = False
        return validSimFile