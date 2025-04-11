import os.path

from md_readers import data_txt_reader as datatxt
from md_readers import dump_txt_reader as dumptxt

filetypes = {
    "data",
    "dump"
}

def check_path(path):
    if path is None:
        raise Exception("Path not provided")
    elif not os.path.isfile(path):
        raise Exception("No file was found at the specified path")
    elif get_filetype(path) not in filetypes:
        raise Exception("Data file type extnension not recognized")
    
def get_filetype(path):
    return str.split(path, ".")[-1]

def read_header(path):
    check_path(path)
    filetype = get_filetype(path)
    if filetype == "data":
        return datatxt.read_header(path)
    elif filetype == "dump":
        return dumptxt.read_header(path)
    return

def read_atoms(path):
    check_path(path)
    filetype = get_filetype(path)
    if filetype == "data":
        return datatxt.read_atoms(path)
    elif filetype == "dump":
        return dumptxt.read_atoms(path)
    return