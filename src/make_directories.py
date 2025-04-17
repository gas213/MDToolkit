import os.path

def make_directories(data_path):
    """
    Creates folder structure for outputting results.\n
    Example using file named 69.data:\n
    - {directory containing 69.data}/
    \t- analysis/
    \t\t- 69/
    \t\t\t- profiles/
    """

    dir_root = os.path.dirname(os.path.abspath(data_path))
    dir_analysis = os.path.join(dir_root, "analysis")
    if not os.path.isdir(dir_analysis): os.makedirs(dir_analysis)

    data_filename = os.path.split(data_path)[-1]
    dir_results = os.path.join(dir_analysis, str.split(data_filename, ".")[0])
    dir_profiles = os.path.join(dir_results, "profiles")
    if os.path.isdir(dir_results):
        raise Exception(f"Directory already exists: {dir_results}")
    else:
        os.makedirs(dir_results)
        os.makedirs(dir_profiles)

    return dir_results