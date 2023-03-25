import os
import datetime

def image_timestamp():
        file_path = 'final_image.png'
        if os.path.exists(file_path):
            modified_time = os.path.getmtime(file_path)
            modified_time_str = datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f'The file was last modified on {modified_time_str}.')
        else:
            print('The file does not exist.')