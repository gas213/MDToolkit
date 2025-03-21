import os.path

def check_path(path):
    if path is None:
        raise Exception("Path not provided")
    elif not os.path.isfile(path):
        raise Exception("No file was found at the specified path")