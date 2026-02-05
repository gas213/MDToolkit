import os.path

def make_initial_dirs(data_path: str, step_start: int, step_end: int):
    path_source = os.path.dirname(data_path)
    path_analysis = os.path.join(path_source, "analysis")
    if not os.path.isdir(path_analysis): os.makedirs(path_analysis)

    if step_start != step_end:
        prefix = os.path.basename(data_path).split("*")[0]
        path_unique = os.path.join(path_analysis, f"{prefix}{step_start}_{step_end}")
    else:
        path_unique = os.path.join(path_analysis, str.split(os.path.basename(data_path), ".")[0])

    if os.path.isdir(path_unique):
        raise Exception(f"Directory already exists: {path_unique}")
    else:
        os.makedirs(path_unique)