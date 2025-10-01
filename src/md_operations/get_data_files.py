import glob
import os.path

def get_data_files(data_path: str, step_start: int, step_end: int) -> list[str]:
    is_multi_file: bool = False
    
    filename_stripped = os.path.splitext(os.path.basename(data_path))[0]
    if ("*" in filename_stripped):
        is_multi_file = True
        if step_start is None:
            raise Exception("Missing value for step_start")
        elif step_end is None:
            raise Exception("Missing value for step_end")
        elif filename_stripped.count("*") > 1:
            raise Exception("Cannot have multiple wildcards (*) in data_path value")
        elif step_start > step_end:
            raise Exception("Value of step_start must be less than or equal to step_end")
    elif not os.path.isfile(data_path):
        raise Exception(f"No data file was found at the specified path: {data_path}")

    data_files: list[str] = []
    if is_multi_file:
        path_before_wildcard = data_path.split("*")[0]
        path_after_wildcard = data_path.split("*")[1]
        wildcard_matches = glob.glob(data_path)
        valid_step_numbers: list[int] = []
        # Order data files by step number
        for match in wildcard_matches:
            step_str = match.replace(path_before_wildcard, "").replace(path_after_wildcard, "")
            if step_str.isdigit() and int(step_str) >= step_start and int(step_str) <= step_end:
                valid_step_numbers.append(int(step_str))
        valid_step_numbers.sort()
        if len(valid_step_numbers) == 0:
            raise Exception(f"No data files were found matching the specified pattern of {data_path} while having a step number in the range of {step_start} through {step_end}")
        for step in valid_step_numbers:
            data_files.append(path_before_wildcard + str(step) + path_after_wildcard)
    else:
        data_files.append(data_path)

    return data_files