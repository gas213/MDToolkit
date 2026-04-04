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

state.md_logger.log("ANALYSIS COMPLETE")