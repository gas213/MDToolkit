import os.path

def make_directories(data_path):
    dir_data = os.path.dirname(os.path.abspath(data_path))
    dir_analysis = os.path.join(dir_data, "analysis")
    if not os.path.isdir(dir_analysis): os.makedirs(dir_analysis)

    data_filename = os.path.split(data_path)[-1]
    dir_write = os.path.join(dir_analysis, str.split(data_filename, ".")[0])
    if os.path.isdir(dir_write): raise Exception(f"Directory already exists: {dir_write}")
    else: os.makedirs(dir_write)

    return dir_write