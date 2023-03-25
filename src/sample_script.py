import Blackboard
import time
import ast

Blackboard.setup(4, 1)
start = time.time()
Blackboard.main_loop()
end = time.time()

grab = Blackboard.current_best
error = Blackboard.current_error
learner_name = grab[0]
learner_obj = grab[1]
print("We found the best learner in " + str(end-start) + " seconds")
print("the best learner is the " + learner_name + " model, with an average absolute error of " + str(error))

pred = input()
while pred != "Quit":
    try:
        pred_input = ast.literal_eval(pred)
    except:
        print("Whoops! Formatting error")
        pred = input()
        continue
    
    print(learner_obj.predict(pred_input))
    
    input = input()