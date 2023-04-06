import os
def get_path():
    p = os.getcwd()
    tail = 'src'
    if p.endswith('src'):
        tail = ''
        
    return os.path.join(p, tail)

local_path = get_path()

print(local_path)