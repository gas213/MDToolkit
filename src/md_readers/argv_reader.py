import os.path

def read_data_path(args):
    if args is None: raise Exception("Command line arguments not found")
    if len(args) != 2: raise Exception("Wrong number of command line arguments given (should only be one arg - the LAMMPS data file)")

    data_path = args[1]
    if not os.path.isfile(data_path): raise Exception("No file was found at the path specified in the argument")
    
    return data_path