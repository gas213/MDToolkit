import os.path
import sys

from input_interpreter import InputInterpreter
from session_state import SessionState

input_path = sys.argv[1]
input = []
with open(input_path, "r") as file:
    for line in file:
        input.append(line.strip())

state = SessionState()
interpreter = InputInterpreter(input)
interpreter.run(state)

# TODO: this is a workaround
# path_test = os.path.join(path_analysis, "test.txt")
# if os.path.exists(path_test): raise Exception(f"Output file already exists, please rename/move/delete it: {path_test}")
# with open(path_test, "w") as test_file:
#     test_file.writelines([f"{k} {v}\n" for k, v in state.radial_profile.items()])

state.logger.debug("ANALYSIS COMPLETE")