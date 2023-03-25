import os
import importlib
import learner_template
import json
import tensorflow as tf
import firestore as fs
import time
import learner_linked_list
import ast
from statistics import mean
import shutil
import copy
import numpy as np

# GLOBAL STATIC VARIABLES----------------------------
required_performance_streak = 5
required_streak_to_prune = 5
ping_frequency_in_seconds = 15
#----------------------------------------------------

# GLOBAL DYNAMIC VARIABLES---------------------------
local_path = os.path.join('src')

#list of tuples of shape (model name, learner Obj)
valid_models = None
input_num = None
output_num = None
data = None

#tuple of shape (model name, learner Obj)
current_best = None
current_error = None
#----------------------------------------------------

def setup(num_in, num_out):
    global input_num, output_num, valid_models
    model_classes = []
    input_num = num_in
    output_num = num_out

    target_dir = os.path.join(os.getcwd(), local_path,'valid_models')
    python_files = [file[:-3] for file in os.listdir(target_dir) if file.endswith('.py')]

    for file_name in python_files:
        try:
            import_path = os.path.join('valid_models', file_name).replace(os.sep, '.')
            lib = importlib.import_module(import_path)
            camel_case_class_name = file_name.title().replace('_', '')
            learner = getattr(lib, camel_case_class_name)
            if issubclass(learner, learner_template.LearnerTemplate):
                    model_classes.append((file_name, learner))
            else:
                print('The file ' + file_name + '.py is not a valid learner module and will be ignored')
        except Exception as e:
            print("Triggered the following exception when attempting to import file " + file_name + ": \n" + str(e))
    

    json_path = os.path.join(local_path, 'valid_models', 'startup_data.json')
    
#need to handle when json file is empty
    temp = []
    for model_type in model_classes:
        with open(json_path, "r") as file:
            loaded_data = json.load(file)
        print("Data")
        print(loaded_data)
        exists_in_json = True
        if model_type[0] in loaded_data:
            model_metadata = ast.literal_eval(loaded_data[model_type[0]])
            stack_pointer, current_threshold, performance_count = model_metadata[0], model_metadata[1], model_metadata[2]
        else:
            stack_pointer, current_threshold, performance_count = 0, None, 0
            exists_in_json = False
        constructor = model_type[1]
        is_model_valid, model = is_model_valid_learner(model_type[0], constructor, stack_pointer, current_threshold, performance_count, input_num, output_num)

        if is_model_valid:
            temp.append((model_type[0], model))
            if not(exists_in_json):
                new_data = {model_type[0]: str([stack_pointer, model.current_threshold, performance_count])}
                print(new_data)
                print({**loaded_data, **new_data})
                with open(json_path, "w") as file:
                    json.dump({**loaded_data, **new_data}, file)

    valid_models = learner_linked_list.LearnerLinkedList(temp)

def is_model_valid_learner(model_name, constructor, stack_pointer, current_threshold, performance_count, input_num, output_num):
    try:
        model = constructor(stack_pointer, current_threshold, performance_count, input_num, output_num)
        return True, model
    except TypeError:
        print('The model ' + model_name + ' does not comply with the standard machine learner template, and will not be executed.')
        return False, None
    
def save_best_weights():
    save_path = get_current_best_path()
    current_best[1].get_model().save_weights(save_path)

def is_best_present():
    return os.path.exists(local_path, 'current_best', 'best_weights.h5')

def get_current_best_path():
    return os.path.join(local_path, 'current_best', 'best_weights.h5')

def main_loop():
    global valid_models, current_best, data, current_error

    if valid_models.active_count == 0:
        print("No valid models present!")
        return
    
    #current_best = ##don't think we need to start by setting this 
    while not(stop_condition()):
        
        data_entries_required = find_smallest_data_requirement()
        count = fs.check_count()
        while count < data_entries_required:
            time.sleep(ping_frequency_in_seconds)
            count = fs.check_count()

        i = 1     
        data = fs.batched_read() ## sync with eric for reading from most recent spot - current_model.stack_pointer 
        print('\n Length of data is: ' + str(len(data[0])))

        x = np.array(data[0]).astype(np.float32, copy=False)
        y = np.array(data[1]).astype(np.float32, copy=False)

        valid_models.active = valid_models.head
        while i <= valid_models.active_count:
            valid_models.next()
            current_learner_obj = valid_models.active.data[1]
            current_learner_name = valid_models.active.data[0] ## sync with eric - need to share with frontend

            if not(current_learner_obj.setup()):
                print("Tensorflow error encountered. Make sure all dependencies are up to date.")
                return 
            
            current_learner_obj.run(count, x, y)
            performance = mean(current_learner_obj.history.val_losses)
        ## sync with eric - send this mean to him and / or the DB

        ## update object with new stack_pointer and performance stat (after comparing to current best)
        ## then update json file with these values, including new threshold, and update max weights as necessary
            current_learner_obj.increase_threshold()
            current_learner_obj.stack_pointer = count

            if current_best == None:
                current_best = (current_learner_name, copy.copy(current_learner_obj))
                current_error = performance

                update_learner_entries(current_learner_name, data=[count, current_learner_obj.current_threshold, 0])
                valid_models.next()
                save_best_weights()
                i += 1

            ##we're doing some unnecessary work here
            elif current_error > performance:
                if current_learner_name == current_best[0]:
                    current_best[1].model = current_learner_obj.get_model()



                    current_best[1].performance_count += 1
                    update_learner_entries(current_best[0], data=[count, current_learner_obj.current_threshold, current_best[1].performance_count])
                
                else:
                    current_best[1].performance_count = 0
                    update_learner_entries(current_best[0], data=[current_best[1].stack_pointer, current_best[1].current_threshold, 0])

                    current_best = (current_learner_name, copy.copy(current_learner_obj))

                    current_learner_obj.performance_count = 0
                    update_learner_entries(current_learner_name, data=[count, current_learner_obj.current_threshold, 0])

                current_error = performance
                valid_models.next()
                save_best_weights()
                i += 1

            else:
                if current_learner_name == current_best[0]:
                    i += 1
                    valid_models.next()
                    
                    update_learner_entries(current_best[0], data=[count, current_learner_obj.current_threshold, current_best[1].performance_count])
                    if valid_models.active_count == 1: ## if we get worse when we have our last contender, leave
                        current_learner_obj.model = None
                        return
                    
                else:
                    current_learner_obj.performance_count += 1
                    current_best[1].performace_count += 1
                    if current_learner_obj.performance_count >= required_streak_to_prune:
                        prune(current_learner_name)
                        valid_models.remove_active()
                    update_learner_entries(current_learner_name, data=[count, current_learner_obj.current_threshold, current_learner_obj.performance_count])
                    update_learner_entries(current_best[0], data=[current_best[1].stack_pointer, current_best[1].current_threshold, current_best[1].performance_count])
                    
            current_learner_obj.model = None
            current_best[1].update_graphs(count)
            update_best_learner_file()

def prune(name):
    source_path = os.path.join(local_path, 'valid_models', name + '.py')
    destination_path = os.path.join(local_path, 'invalid_models', name + '.py')

    try:
        shutil.move(source_path, destination_path)
    except FileNotFoundError:
        pass

def stop_condition():
    return current_best != None and valid_models.active_count == 1 and current_best[1].performance_count > required_performance_streak

##find smallest data requirement of all learners - assumes at least 1 learner present
def find_smallest_data_requirement():
    if(valid_models.active == valid_models.head):
        valid_models.next()
    min_threshold = valid_models.active.data[1].current_threshold
    for i in range(1, valid_models.active_count):
        thresh_compare = valid_models.active.data[1].current_threshold
        if thresh_compare < min_threshold:
            min_threshold = thresh_compare
        valid_models.next()
    
    return min_threshold

def update_learner_entries(current_learner_name, data):
    json_path = os.path.join(local_path, 'valid_models', 'startup_data.json')
    with open(json_path, "r") as file:
        loaded_data = json.load(file)

    new_data = {current_learner_name: str(data)}
    with open(json_path, "w") as file:
            json.dump({**loaded_data, **new_data}, file)

def update_best_learner_file():
    current_name = get_best_model_name()
    new_name = current_best[0]

    if current_name != new_name:
        set_best_model_name(new_name)

def get_best_model_name():
    source_path = os.path.join(local_path, 'current_best', 'best.txt')
    with open(source_path, 'r') as file:
        contents = file.read()
    return contents

def set_best_model_name(name):
    source_path = os.path.join(local_path, 'current_best', 'best.txt')
    with open(source_path, 'w') as file:
        file.write(name)


# print(get_best_model_name())
# set_best_model_name('teehee')
# print(get_best_model_name())
# print(setup(2,3))
# print(valid_models)
# print(valid_models.next().data)
# print("---------------------------")
# valid_models.print_list()
# valid_models.active.data[1].setup()
# print(valid_models.active.data[1].model)

# prune('linear_fit')

setup(4,1)
main_loop()