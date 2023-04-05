##File to open matlab engine and to calculate the true output
##Purpose: GUI Table 2: User inputs; compare tnesorflow model prediction vs actual matlab output
import matlab.engine 
import os



def calculate(matlab_sim_filename, GUI_user_inputs):

        #matlab files should be stored in src/matlab, add this to the matlab path
        eng = matlab.engine.start_matlab()
        path = os.path.join(os.getcwd(),'matlab')
        eng.addpath(path,nargout=0)
        
        #hard-coded grab user input
        A= GUI_user_inputs[0]
        B= GUI_user_inputs[1]
        C= GUI_user_inputs[2]
        D= GUI_user_inputs[3]

        # Load the script into the MATLAB workspace
        try:
            output = getattr(eng,matlab_sim_filename)(A,B,C,D,nargout=1) #equivalent to eng.filename(A,B,C,D,nargout=1), but is dynamic
            eng.quit()
            return output
        except Exception as e:
            return Exception
            print(e)

#print(matlab_calculate('unknown_poly_type',[1,1,1,1]))

