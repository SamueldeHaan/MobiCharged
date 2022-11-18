import matlab.engine
eng = matlab.engine.start_matlab()

eng = matlab.engine.start_matlab()
s = eng.genpath('src')
eng.addpath(s, nargout=0)

eng.sample_simulation1(nargout=0)
eng.quit()  