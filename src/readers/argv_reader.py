import os.path

from constants import analysis_filetype

def read_data_path(args):
    if args is None:
        raise Exception("Command line arguments not found")
    if len(args) != 2:
        raise Exception("Wrong number of command line arguments given (should only be one arg - the LAMMPS data file)")

    data_path = args[1]
    if not os.path.isfile(data_path):
        raise Exception("No LAMMPS data file was found at the path specified in the argument")

    analysis_path = data_path + analysis_filetype
    if os.path.isfile(analysis_path):
        raise Exception("Analysis file already exists for this data file; either move, rename or delete the existing one")
    
    return data_path