import os
import importlib
import learner_template
import json

# global variables

#tuple of form (learner name, learner class reference) - can check local json file for learner name, get its stack_pointer (how much its seen) 
# and current threshold (how much it needs to see before it runs again)
model_classes = []
valid_models = []

##might not need these permeated - depends on if we rebuild the learner object every time 
input_num = None
output_num = None

def setup(num_in, num_out):
    global input_num, output_num
    input_num = num_in
    output_num = num_out

    target_dir = os.path.join(os.getcwd(), 'src','valid_models')
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
    

    json_path = os.path.join('src', 'valid_models', 'startup_data.json')
    
#need to handle when json file is empty
    for model_type in model_classes:
        with open(json_path, "r") as file:
            loaded_data = json.load(file)
        print("Data")
        print(loaded_data)
        exists_in_json = True
        if model_type[0] in loaded_data:
            model_metadata = loaded_data[model_type[0]]
            stack_pointer, current_threshold, performance_count = model_metadata[0], model_metadata[1], model_metadata[2]
        else:
            stack_pointer, current_threshold, performance_count = 0, None, 0
            exists_in_json = False
        constructor = model_type[1]
        is_model_valid, model = is_model_valid_learner(model_type[0], constructor, stack_pointer, current_threshold, performance_count, input_num, output_num)

        if is_model_valid:
            valid_models.append(model)
            if not(exists_in_json):
                new_data = {model_type[0]: str([stack_pointer, current_threshold, performance_count])}
                print(new_data)
                print({**loaded_data, **new_data})
                with open(json_path, "w") as file:
                    json.dump({**loaded_data, **new_data}, file)


def is_model_valid_learner(model_name, constructor, stack_pointer, current_threshold, performance_count, input_num, output_num):
    try:
        model = constructor(stack_pointer, current_threshold, performance_count, input_num, output_num)
        return True, model
    except TypeError:
        print('The model ' + model_name + ' does not comply with the standard machine learner template, and will not be executed.')
        return False, None


print(setup(2,3))
print(model_classes)
print(valid_models)

##still need to check if is instance of LearnerTemplate

import ast

# Define a string representation of a list
str_list = "[1, 2, 3, 'four', 'five']"

# Use ast.literal_eval() to convert the string to a list
list_obj = ast.literal_eval(str_list)

# Now you have a list object that you can work with
print(list_obj)  # Output: [1, 2, 3, 'four', 'five']