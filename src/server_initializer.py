
import firestore 
def main():
    current_count = firestore.check_count()
    print("CURRENT COUNT = ", current_count)
    inputList = []
    inputSizeGood = False
    outputSizeGood = False

    while not(inputSizeGood):
        inputSize = input("Please Enter The Number of Unique Elements in the Input: ")
        if(inputSize.isdecimal()):
            inputSizeGood = True
        else:
            print("Please Enter an Integer Value!")
    
    while not(outputSizeGood):
        outputSize = input("Please Enter The Number of Unique Elements in the Output: ")
        if(outputSize.isdecimal()):
            outputSizeGood = True
        else:
            print("Please Enter an Integer Value!")
    
    for numIn in range(int(inputSize)): 
        inputRanges = False
        inputRangeMin = False
        inputRangeMax = False
        while not(inputRanges):
            while not(inputRangeMin):    
                rangeMin = input(f"Please Enter the Minimum Value in the Range (input #{numIn + 1}): ")
                if(rangeMin.isdecimal()):
                    inputRangeMin = True
                else:
                    print("Please Enter an Integer or Float Value")
            while not(inputRangeMax):
                rangeMax = input(f"Please Enter the Maximum Value in the Range (input #{numIn + 1}): ")
                if(rangeMax.isdecimal()):
                    tempList = [rangeMin, rangeMax]
                    inputList.append(tempList)
                    inputRangeMax = True
                else:
                    print("Please Enter an Integer or Float Value")
                inputRanges = True
    
    #print(inputList)
    startServer(inputSize, outputSize, inputList)

def startServer(inputSize, outputSize, inputList):
    import server
    server.Server_Configuration(inputSize,outputSize, inputList)
    



main()