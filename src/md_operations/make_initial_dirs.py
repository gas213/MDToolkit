import os.path

def make_initial_dirs(data_path: str, step_start: int, step_end: int) -> str:
    source_path = os.path.dirname(data_path)
    analysis_path = os.path.join(source_path, "analysis")
    if not os.path.isdir(analysis_path): os.makedirs(analysis_path)

    if step_start != step_end:
        prefix = os.path.basename(data_path).split("*")[0]
        results_path = os.path.join(analysis_path, f"{prefix}{step_start}_{step_end}")
    else:
        results_path = os.path.join(analysis_path, str.split(os.path.basename(data_path), ".")[0])

    if os.path.isdir(results_path):
        raise Exception(f"Directory already exists: {results_path}")
    else:
        os.makedirs(results_path)

    return results_path