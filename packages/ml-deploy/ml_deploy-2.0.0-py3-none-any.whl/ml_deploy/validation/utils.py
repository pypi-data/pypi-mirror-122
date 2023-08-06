import os

def is_file_exists(path:str)->bool:
    if os.path.isfile(path):
        return True
    return False