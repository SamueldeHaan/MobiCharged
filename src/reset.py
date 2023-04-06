import os
import json
import shutil


confirm = str(input("Do you wish to reset the current best model. The discovered weights will be deleted and all models deemed invalid will regain their validity. Input Y to confirm, anything else to return"))
if confirm == "Y":
    pass

else:
    local_path = os.path.join('src')

    target_dir = os.path.join(os.getcwd(), local_path,'invalid_models')
    print(target_dir)
    python_files = [file[:-3] for file in os.listdir(target_dir) if file.endswith('.py')]

    for name in python_files:

        source_path = os.path.join(local_path, 'invalid_models', name + '.py')
        destination_path = os.path.join(local_path, 'valid_models', name + '.py')

        try:
            shutil.move(source_path, destination_path)
        except FileNotFoundError:
            pass
        
    weights = os.path.join(local_path, 'current_best', 'best_weights.h5')
    if os.path.exists(weights):
        os.remove(weights)

    current_error_path = os.path.join(local_path,'current_best','current_error.txt')
    if os.path.exists(current_error_path):
        os.remove(current_error_path)
        
    json_path = os.path.join(local_path, 'valid_models', 'startup_data.json')
    with open(json_path, "w") as file:
        json.dump({}, file)
        
    source_path = os.path.join(local_path, 'current_best', 'best.txt')
    with open(source_path, 'w') as file:
        file.write('')